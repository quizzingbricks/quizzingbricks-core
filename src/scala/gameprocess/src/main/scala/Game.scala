import akka.zeromq._
import akka.util.ByteString
import akka.actor._
import scala.collection.mutable.HashMap
import scala.concurrent.duration._
import scala.slick.driver.PostgresDriver.simple._
import scala.util.Random

object Game
{
    val sideLength = 8
}

/**
 * Akka actor representing each active game that handles game logic and messaging. The optional arguemnts to the
 * constructor allows the creation of an actor representing a game in progress.
 * @param gameId    The unique id of the game.
 * @param playerIds The user ids of the players that are in this game.
 * @param players   Optional list of full information of the players.
 * @param boardArg  Optional array that represents the bricks currently on the board, given as a flat list of player
 *                  ids, where each player id corresponds to the brick it has laid down. The first k elements of 
 *                  boardArg is the top row of k bricks on the board, and so on down to the bottom row.
 */
class Game (gameId: Int, playerIds: List[Int], publisher: ActorRef, players: List[Player] = Nil, boardArg: Array[Int] = null) extends Actor
{
    val db = Database.forURL("jdbc:postgresql://localhost:5432/quizzingbricks_dev", 
                             driver = "org.postgresql.Driver", user = "qb", password = "qb123")
    var board: Array[Int] = null
    var playerMap: HashMap[Int, Player] = null
    var playerList: List[Player] = null
    
    /**
     * Sets up the game information according to the information given in the class header comment.
     */
    override def preStart()
    {
        if(boardArg != null)
            board = boardArg.clone()
        else
        {
            board = new Array[Int](Game.sideLength*Game.sideLength)
            for (i <- 0 to board.length-1)
                board(i) = 0
        }
        playerMap = new HashMap[Int, Player]()
        if(players != Nil)
            for(p <- players)
                playerMap.put(p.userId, p)
        else
            for (p <- playerIds)
                playerMap.put(p, new Player(p, Player.PLACING))
        playerList = (playerIds map (id => playerMap(id))).toList
    }
    
    /**
     * Checks if a proposed move is valid.
     * @param x The x coordinate of the move.
     * @param y The y coordinate of the move.
     * @return True if the move is valid, false if not. 
     */
    def isValidMove(x: Int, y: Int) = x >= 0 && x < Game.sideLength && y >= 0 && y < Game.sideLength && 
                                                board(y*Game.sideLength + x) == 0
    
    /**
     * Constructs a GameMessage containing all information about the game.
     * @return a GameMessage containing all information about the game.
     */
    def getGameInfo() = GameMessage(gameId, playerList map (_.toMessage), board)
    
    /**
     * Partitions a list of elements into a list of lists of elements in O(n^2) time.
     * @param l The list to partition.
     * @param f The property to partition by given by a function taking two elements, returning true if these
     *          elements belong to the same partition.
     * @return The list of partitioned lists.
     */
    def partitionSeveral[A](l: List[A], f: ((A,A) => Boolean)) : List[List[A]] =
    {
        l match
        {
            case Nil =>   Nil
            case x::xs => val (a,b) = l partition (f (x,_))
                          a :: partitionSeveral(b, f)
        }
    }
    
    /**
     * Sends ZMQ PUB messages.
     * @param m The ZMQ pub message to send.
     */
    def publishMessage(m: PublishMessage)
    {
        val (id, msg) = MessageTranslator.translate(m)
        
        publisher ! ZMQMessage(ByteString("game-" + gameId), ByteString(id.toString()), msg)
    }
    
    /**
     * Checks if a player needs to answer additional questions to continue the game, and updates the player infos
     * accordingly. 
     */
    def updateQuestionStates()
    {
        // We can only give players a new round of questions if every player has chosen where to place their brick
        if(!playerList.forall(p => p.state >= Player.PLACED))
            return
        
        // First, partition the players into sites, where each site is a list of all the players who have placed their
        // bricks on the same place
        val sites = partitionSeveral(playerList, (p1: Player, p2: Player) => p1.x == p2.x && p1.y == p2.y)
        // For each site where everyone has answered their question (or timed out)
        for(site <- sites if site.forall(p => p.state == Player.ANSWERED))
        {
            val correctAnswerers = site.filter(p => p.answer == p.question.correctAnswer)
            // If there are more than two players who have answered correctly .. 
            if(correctAnswerers.length > 1)
            {
                for(c <- correctAnswerers)
                {
                    // .. then every such player must now ask for another question
                    c.resetTo(Player.PLACED)
                    publishMessage(PlayerStateChangePubSubMessage(c.toMessage))
                    db withSession 
                    {   implicit session: Session =>
                        val q = Query(PlayersGamesTable).filter(g => g.playerId === c.userId && g.gameId === gameId)
                                .map(p => p.state ~ p.question ~ p.alt1 ~ p.alt2 ~ p.alt3 ~ p.alt4 ~ p.answer)
                        q.update(Player.PLACED, "", "", "", "", "", 0)
                    }
                }
            }
        }
    }
    
    /**
     * Called when a player has asked to place a brick somewhere.
     * @param playerId The user id of the player.
     * @param x The x coordinate of the brick placement.
     * @param y The y coordinate of the brick placement.
     */
    def handleMoveRequest(playerId: Int, x: Int, y: Int)
    {
        val player = playerMap(playerId)
        
        // player.state > 0 means either PLACED, ANSWERING or ANSWERED, meaning we have already placed a brick this turn
        if(!isValidMove(x, y) || player.state > 0)
        {
            sender ! GameError("The move is not allowed", 250)
            return;
        }
        
        player.state = Player.PLACED
        player.x = x
        player.y = y
        publishMessage(PlayerStateChangePubSubMessage(player.toMessage))
        
        db withSession 
        {
            implicit session: Session =>
            val q = Query(PlayersGamesTable).filter(g => g.playerId === playerId && g.gameId === gameId)
                                            .map(p => p.x ~ p.y ~ p.state)
            q.update((x,y, Player.PLACED))
        }
        
        // This move might enable players in other sites to ask for another question, if this player has made a move
        // somewhere else
        updateQuestionStates()
        
        sender ! MoveResponse()
    }
    
    /**
     * Callback for when the timeout for answering a question is triggered.
     * @param player The user id of the player who was supposed to answer the question.
     */
    def questionTimeout(player: Int)
    {
        playerMap(player).state match
        {
            case Player.ANSWERING =>
                println("Player " + player + " timed out to answer question.")
                handleAnswerRequest(gameId, player, 0)
            case _ =>
                println("Question timeout while player not in AnsweringQuestion state!")
        }
    }
    
    /**
     * Handles the request of a player to be given a question to answer.
     * @param player The player who made the request.
     */
    def handleQuestionRequest(playerId: Int)
    {
        val player = playerMap(playerId)
        
        // If the player is answering a question, we simply retransmit the question he is supposed to answer
        if(player.state == Player.ANSWERING)
        {
            sender ! QuestionResponse(player.question.question, player.question.alternatives)
            return
        }
        if(player.state != Player.PLACED)
        {
            sender ! GameError("Question is not allowed in the present state", 300)
            return
        }
            
        var minId, maxId: Option[Int] = None

        db withSession 
        {   implicit session: Session =>
            minId = Query(QuestionsTable.map(_.questionId).min).first
            maxId = Query(QuestionsTable.map(_.questionId).max).first
            
            (minId, maxId) match
            {
                case (Some(minId), Some(maxId)) =>
                    // Find a random question to ask. This method does not necessitate that the autoinc index variable
                    // runs from 1 to max unbrokenly, but for every question that has been removed, the result is less
                    // randomly distributed.
                  
                    // First, generate a random number between minId and maxId
                    val rnd = new Random(System.currentTimeMillis())
                    val rn = minId + rnd.nextInt(1 + maxId - minId)
                
                    // Pick the first question with id greater than the random number generated. Since this asks the 
                    // database to find a table every such question, it is unnecessarily slow so this can be improved 
                    val q = (for {
                        p <- QuestionsTable if p.questionId >= rn
                    } yield (p.question, p.alt1, p.alt2, p.alt3, p.alt4, p.answer))
                      .list.map({case (a,b,c,d,e,f) => Question(a, List(b,c,d,e), f)}).head

                    import context.dispatcher
                    // Give the player a certain amount of time to answer the question
                    val pendingTimeout = context.system.scheduler.scheduleOnce(10 seconds, self, ("timeout", playerId))
                      
                    player.state = Player.ANSWERING
                    player.pendingTimeout = pendingTimeout
                    player.question = q
                    publishMessage(PlayerStateChangePubSubMessage(player.toMessage))
                    
                    // If the database crashes after a player has been posed a question, he will not have
                    // a timer when the game process is restored and the information is retrieved from the database, 
                    // so effectively he will have an infinite amount of time to answer a question, but I suppose he 
                    // deserves it in that case
                    val r = Query(PlayersGamesTable).filter(g => g.playerId === playerId && g.gameId === gameId)
                            .map(p => p.state ~ p.question ~ p.alt1 ~ p.alt2 ~ p.alt3 ~ p.alt4 ~ p.correctAnswer)
                    r.update((Player.ANSWERING, q.question, q.alternatives(0), 
                              q.alternatives(1), q.alternatives(2), q.alternatives(3), q.correctAnswer))
                    sender ! QuestionResponse(q.question, q.alternatives)
                case _ =>
                    sender ! GameError("No questions in database!", 0)
                    return
            }
        }
    }
    
    /**
     * Handles a GameInfoRequest request sent to this game.
     * @param idReq The id of the game whose game information was requested. Hopefully the same as the id of this game.
     */
    def handleGameInfoRequest(idReq: Int)
    {
        assert(idReq == gameId)
        sender ! GameInfoResponse(getGameInfo())
    }
    
    /**
     * Handles a request to answer a question that was given.
     * @param gameId The id of the game the request was sent to. Hopefully the same as the id of this game.
     * @param playerId The id of the player who sent the request.
     * @param answer The answer alternative given as the answer to the question, or 0 if this is part of a timeout 
     *               callback.
     */
    def handleAnswerRequest(gameId: Int, playerId: Int, answer: Int)
    {
        val player = playerMap(playerId)
        if(player.state != Player.ANSWERING)
        {
            // This error string assumes that the player was ever given a question to begin with, but hopefully the
            // client keeps track of that.
            sender ! GameError("The answer was too late", 252)
            return;
        }
        
        if(player.pendingTimeout != null)
            player.pendingTimeout.cancel()
        player.state = Player.ANSWERED
        player.answer = answer
        publishMessage(PlayerStateChangePubSubMessage(player.toMessage))
        
        db withSession 
        {   implicit session: Session =>
            val q = Query(PlayersGamesTable).filter(g => g.playerId === playerId && g.gameId === gameId)
                                            .map(p => p.state ~ p.answer)
            q.update((Player.ANSWERED, answer))
        }
        
        // If the answer is 0, it's actually just the timeout callback calling this function, so don't send a message
        if(answer != 0)
            sender ! AnswerResponse(player.question.correctAnswer == answer)
        
        // Check if this answer triggered anyone to be able to ask for another question
        updateQuestionStates()
        
        if(!playerList.forall(p => p.state == Player.ANSWERED))
            return
            
        // Everyone has answered and a new round starts
        for(p <- playerList)
        {
            // Everyone who answered correctly gets their bricks placed. updateQuestionStates() ensures that only one
            // player on each position has done so at this point
            if(p.answer == p.question.correctAnswer)
                board(Game.sideLength*p.y + p.x) = p.userId
            p.resetTo(Player.PLACING)
            
            db withSession 
            {   implicit session: Session =>
                val q = Query(PlayersGamesTable).filter(g => g.gameId === gameId)
                        .map(p => p.x ~ p.y ~ p.state ~ p.question ~ p.alt1 ~ p.alt2 ~ p.alt3
                                  ~ p.alt4 ~ p.correctAnswer ~ p.answer)
                q.update(0, 0, Player.PLACING, "", "", "", "", "", 0, 0)
            }
        }
        db withSession
        {    implicit session: Session =>
             val g = Query(GamesTable).filter(g => g.gameId === gameId).map(g => g.board)
             g.update(board.mkString(","))
        }
        publishMessage(NewRoundPubSubMessage(GameMessage(gameId, playerList map (_ toMessage), board)))
    }
    
    /**
     * Handles incoming messages.
     */
    def receive =
    {
        case m: PlayerRequestMessage =>
            if (!(playerList map (p => p.userId) contains m.userId))
                sender ! GameError("You are not permitted to that game", 251)
            else
            {
                m match 
                {
                    case MoveRequest(_, player, x, y) =>
                        handleMoveRequest(player, x, y)
                    case QuestionRequest(_, player) =>
                        handleQuestionRequest(player)
                    case AnswerRequest(id, playerId, answer) =>
                        // handleAnswerRequest can be called with 0 as an answer, so we need to check this here
                        if(answer < 1 || answer > 4)
                            sender ! GameError("Incorrect answer alternative given", 300)
                        else
                            handleAnswerRequest(id, playerId, answer)
                }
            }
        case GameInfoRequest(idReq) => 
            handleGameInfoRequest(idReq)
        case ("timeout", playerId: Int) =>
            questionTimeout(playerId)            
    }
}