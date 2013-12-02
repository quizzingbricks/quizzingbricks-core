import akka.actor._
import akka.zeromq._
import akka.util.ByteString
import scala.slick.driver.PostgresDriver.simple._

/**
 * Akka actor that handles incoming ZMQ messages concurrently with other such actors, enabling many requests to be
 * handled at any given time. The incoming messages are delivered from the main loop of the GameProcess that serves
 * as a broker between outside processes and BrokerWorkers.
 */
class BrokerWorker (n: Int, gameCache: ActorRef) extends Actor
{
    println("Creating worker #" + n + ".")
   
    val db = Database.forURL("jdbc:postgresql://localhost:5432/quizzingbricks_dev", 
                             driver = "org.postgresql.Driver", user = "qb", password = "qb123")
    val socket = ZeroMQExtension(context.system).newReqSocket(Array(Connect("tcp://127.0.0.1:1235"), Listener(self)))
                        
    Thread.sleep(1000) // Sort of a hack, to make sure the for some reason asynchronous newReqSocket to finish
    
    var senderId = ByteString() // The hash value of the socket at the front end side of the broker that sent the 
                                // message that this worker is currently processing (aka client hash address)
    
    /**
     * Initiates the request/reply chain of this socket by sending the first request message. Every incoming job to this
     * actor is actually a reply, and the result of the job is sent back as another request.
     */
    override def preStart() 
    {
        socket ! ZMQMessage(ByteString("READY"))
        println("Worker #" + n + " sent READY.")
    }
    
    /**
     * Handles the GameListRequest message that asks for a list of full information about every game that a user is in.
     * @param player The user id of the player that we want to send back the information to.
     */
    def handleGameListRequest(player: Int)
    {
        db withSession 
        { implicit session: Session =>
            // First, retrieve all the game ids of the games that the player is in
            var gameIds = (for { p <- PlayersGamesTable if p.playerId === player } yield(p.gameId)).list
            var l: List[GameMessage] = Nil

            // Then, for each gameid, retrieve the information about that game
            for (id <- gameIds)
            {
                val players = (for { p <- PlayersGamesTable if p.gameId === id } 
                                   yield (p.playerId, p.state, p.x, p.y, p.question, p.alt1, p.alt2, p.alt3,
                                          p.alt4, p.correctAnswer, p.answer, p.score)).list
                val strBoard = (for { p <- GamesTable if p.gameId === id} yield (p.board)).list.head 
                val intBoard = strBoard.split(",").map(_.toInt)
                val playermsgs = players.map ({case (id, state, x, y, question, alt1, alt2, alt3, alt4, ans, corAns, score) 
                                               => PlayerMessage(id, state, x, y, question, List(alt1, alt2, alt3, alt4),
                                                                (if (ans == corAns) true else false), score)})
                l = l ::: List[GameMessage](GameMessage (id, playermsgs, intBoard))
            } 

            val rep = GameListResponse(l) 
            val (i, b) = MessageTranslator.translate(rep)
            socket ! ZMQMessage(senderId, ByteString(), ByteString(i.toString), b)
            println("BrokerWorker #" + n + " created and passed back: " + rep)
        }
    }
    
    /**
     * Translates and passes on the outgoing messages that arrives to this worker from a game actor
     * relayed back from the GameCache.
     * @param m The Message passed from inside the game process, going out.
     */
    def handleOutgoingMessage(m: Message)
    {
        val (i, b) = MessageTranslator.translate(m)
        socket ! ZMQMessage(senderId, ByteString(), ByteString(i.toString), b)
        println("BrokerWorker #" + n + " got back a message and passed it on: " + m)
    }

    /**
     * Handles incoming messages in the form of ZMQMessages, and outgoing messages in the form of Messages.
     */
    def receive = 
    {
        case m: ZMQMessage =>
            // The incoming message is of the form:
            // client hash address | protocol id | protocol message
            assert(m.frames.length == 3)
            senderId = m.frames(0)
            val id = m.frames(1).decodeString("UTF-8").toInt
            val msgByteString = m.frames(2)
            var msg = MessageTranslator.translate(id, msgByteString)

            msg match 
            {
                case GameListRequest (player) =>
                    handleGameListRequest(player)                
                case _ => 
                    println("BrokerWorker #" + n + " passing on a message to the game cache: " + msg)
                    gameCache ! msg
            }
        case m: Message =>
            handleOutgoingMessage(m)
    }
}