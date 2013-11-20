abstract class Message // General messages to the game module
{
}

abstract class GameRequestMessage extends Message // Incoming messages to a specific game
{
    val gameId: Int = 0
}

abstract class PlayerRequestMessage extends GameRequestMessage
{
    val userId: Int = 0
}

abstract class ReplyMessage extends Message // Outgoing messages
{
}

case class GameMessage(gameId: Int, players: List[PlayerMessage], board: Array[Int]) extends ReplyMessage
{
    //override def toString() = "GameMessage { gameId: " + gameId + ", players: (" + players.mkString(", ") + "), board: (" + board.mkString(", ") + ") }"
    override def toString() = 
    {
        var str: String = "\nGameMessage (id: " + gameId + ")\n" + players.mkString("\n") + "\nboard:\n"
        for(y <- 0 to 7)
        {
            for(x <- 0 to 7)
            {
                str += board(y*8 + x).toString() + "\t"
            }
            str += "\n"
        }
        str
    }
}

case class CreateGameRequest(players: Array[Int]) extends GameRequestMessage
{
    override def toString() = "CreateGame {players: (" + players.mkString(", ") + ") }"
}

case class CreateGameResponse(gameId: Int) extends ReplyMessage
{
    override def toString() = "CreateGameResponse { gameId: " + gameId + " }"
}

case class GameInfoRequest(override val gameId: Int) extends GameRequestMessage
{
    override def toString() = "GameInfoRequest { gameId: " + gameId + " }"
}

case class GameInfoResponse(game: GameMessage) extends ReplyMessage
{
    override def toString() = "GameInfoResponse { game: " + game + " }"
}

case class GameListRequest(userId: Int) extends Message
{
    override def toString() = "GameListRequest { userId: " + userId + " }"
}

case class GameListResponse(gameList: List[GameMessage]) extends ReplyMessage
{
    override def toString() = "GameListMessage { gameList: " + gameList.mkString(", ") + " }"
}

case class PlayerMessage(userId: Int, state: Int, x: Int, y: Int, question: String, alternatives: List[String], answeredCorrectly: Boolean)
{
    //override def toString() = "PlayerMessage { userId: " + userId + ", state: " + Player.stateToString(state) + " x: " + x + ", y: " + y + ", question: " + question + ", alternatives: " + alternatives.mkString + ", answeredCorrectly:  " + answeredCorrectly + " }"
    override def toString() = "player " + userId + " [" + Player.stateToString(state) + "]: " + "(" + x + "," + y + ")\n question: " + question.take(20) + "[...]" + "\n  alternatives: " + alternatives.mkString + "\n  answeredCorrectly " + answeredCorrectly 
}

case class MoveRequest(override val gameId: Int, override val userId: Int, x: Int, y: Int) extends PlayerRequestMessage
{
    override def toString() = "MoveRequest { id: " + gameId + ", userId: " + userId + ", x: " + x + ", y: " + y + " }"
}

case class MoveResponse() extends ReplyMessage
{
    override def toString() = "MoveResponse { }"
}

case class QuestionRequest(override val gameId: Int, override val userId: Int) extends PlayerRequestMessage
{
    override def toString() = "QuestionRequest { gameId: " + gameId + ", userId: " + userId + " }"
}
    
case class QuestionResponse(question: String, alternatives: List[String]) extends ReplyMessage
{
    override def toString() = "QuestionResponse { question: " + question + ", alternatives: (" + alternatives.mkString(", ") +  ") }"
}

case class AnswerRequest(override val gameId: Int, override val userId: Int, answer: Int) extends PlayerRequestMessage
{
    override def toString() = "AnswerRequest { gameId: " + gameId + ", userId: " + userId + ", answer: " + answer + " }" 
}

case class AnswerResponse(correctAnswer: Boolean) extends ReplyMessage
{
    override def toString() = "AnswerResponse { correctAnswer: " + correctAnswer + " }"
}

case class GameError(description: String, code: Int) extends ReplyMessage
{
    override def toString() = "GameError { what: " + description + ", code: " + code + " }"
}



    


