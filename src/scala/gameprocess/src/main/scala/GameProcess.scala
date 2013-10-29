import org.zeromq.ZMQ
import org.zeromq.ZeroMQ
import akka.actor._
import akka.zeromq._
import akka.util.ByteString
import org.zeromq._
import scala.concurrent.Future
import akka.util.Timeout
import scala.concurrent.duration._
import scala.collection.JavaConverters._
import scala.collection.mutable.HashMap
import scala.concurrent.Await

class BrokerWorker (n: Int, gameCache: ActorRef) extends Actor
{
    println("Creating worker #" + n + ".")
   
    val socket = ZeroMQExtension(context.system).newReqSocket(
                        Array(Connect("tcp://127.0.0.1:1235"), Listener(self)))
                        
    Thread.sleep(1000)
    
    //val worker = context.actorOf(Props(classOf[Worker], n, gameCache))
    
    var senderId = ByteString()
    
    override def preStart() 
    {
        socket ! ZMQMessage(ByteString("READY"))
        println("Worker #" + n + " sent READY.")
    }

    def receive = 
    {
        case m: ZMQMessage =>
            assert(m.frames.length == 4) // backend hash id | 0 | protocol id | protocol message
            senderId = m.frames(0)
            val id = m.frames(2).decodeString("UTF-8").toInt
            val msgByteString = m.frames(3)
            var msg = MessageTranslator.translate(id, msgByteString)

            println("BrokerWorker #" + n + " passing on a message to the game cache: " + msg)
            gameCache ! msg
        case m: Message =>
            val (i, b) = MessageTranslator.translate(m)
            socket ! ZMQMessage(senderId, ByteString(), ByteString(i.toString), b)
            println("BrokerWorker #" + n + " got back a message and passed it on: " + m)
    }
}

class Game (id: Int, players: Array[Int]) extends Actor
{
    var board: Array[Int] = new Array(0)
    
    override def preStart()
    {
        board = new Array[Int](8*8)
        for (i <- 0 to board.length-1)
            board(i) = 0
    }
    
    def receive =
    {
        case GameInfoRequest(idReq) => 
            assert(idReq == id)
            sender ! GameInfoReply(id, players, board)
        case PlayerMove(_, player, x, y) =>
            if (! (players contains player))
                sender ! Failure("Moving player not in game")
            else
            {
                board(y*8+x) = player
                sender ! GameInfoReply(id, players, board)
            }
    }
}

class GameCache extends Actor
{
    var hashMap = new HashMap[Int, ActorRef]
    var highestId = 0
    
    def receive =
    {
        case CreateGame (players) =>
            println("GameCache received creategame")
            highestId = highestId + 1
            val game = context.system.actorOf(Props(classOf[Game], highestId, players))
            hashMap.put(highestId, game)
            game forward GameInfoRequest(highestId)
        case x: GameRequestMessage =>
            val game = hashMap.get(x.id)
            game match
            {
                case None => sender ! Failure("Game not found!")
                case Some(g) => g forward x 
            }
    }
}

object GameProcess
{
    def main(args: Array[String]) 
    {
        val back = 0; val front = 1
        
        val system = ActorSystem("zmq")
        val context = ZMQ.context(1)

        val backend  = context.socket(ZMQ.ROUTER)
        val frontend = context.socket(ZMQ.ROUTER)
        
        backend.bind("tcp://*:1235")
        frontend.bind("tcp://*:1234")

        val items = context.poller(2)
        
        items.register(backend, ZMQ.Poller.POLLIN)
        items.register(frontend, ZMQ.Poller.POLLIN) 
        
        val workerQ = scala.collection.mutable.Queue[Array[Byte]]()
        
        val gameCache = system.actorOf(Props(classOf[GameCache]))
        
        for (i <- 0 to 9)
        {
            system.actorOf(Props(classOf[BrokerWorker], i, gameCache))
        }    

        while (true) 
        {
            items.poll
            if(items.pollin(back)) 
            {
                println("Backend received a message!")
                val workerAddr = backend.recv(0)
                assert(backend.hasReceiveMore())
                val nil = backend.recv(0)
                assert(new String(nil) == "" && backend.hasReceiveMore())
                val clientAddr = backend.recv(0)
                
                if(backend.hasReceiveMore())
                {
                    val nil = backend.recv(0)
                    assert(new String(nil) == "" && backend.hasReceiveMore())
                    frontend.send(clientAddr, ZMQ.SNDMORE)
                    frontend.send("".getBytes, ZMQ.SNDMORE)
                    println("Sent to frontend!")
                    do
                    {
                        var msg = backend.recv(0)
                        frontend.send(msg, if (backend.hasReceiveMore) ZMQ.SNDMORE else 0)
                    } while (backend.hasReceiveMore())
                }
                else
                {
                    assert(new String(clientAddr) == "READY")
                    println("Received ready!")
                }
                workerQ.enqueue(workerAddr)
            }
            if(items.pollin(front) && !workerQ.isEmpty)
            {
                println("Frontend received a message")
                val clientAddr = frontend.recv(0)
                assert(frontend.hasReceiveMore())
                val nil = frontend.recv(0)
                assert(frontend.hasReceiveMore() && new String(nil) == "")

                backend.send(workerQ.dequeue, ZMQ.SNDMORE)
                backend.send("".getBytes, ZMQ.SNDMORE)
                backend.send(clientAddr, ZMQ.SNDMORE)
                backend.send("".getBytes, ZMQ.SNDMORE)
                println("Sent to backend!")                
                do
                {
                    var msg = frontend.recv(0)
                    backend.send(msg, if (frontend.hasReceiveMore) ZMQ.SNDMORE else 0)
                } while (frontend.hasReceiveMore())
            }
        }
    }
}