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

case class GameInfoRequest(override val gameId: Int) extends GameRequestMessage
{
    override def toString() = "GameInfoRequest {gameId: " + gameId + "}"
}

case class QuestionMessage(question: String, alternatives: List[String])
{
    override def toString() = "Question { question: " + question + ", alternatives: (" + alternatives.mkString(", ") + ") }"
}

case class PlayerMessage(userId: Int, state: Int, x: Int, y: Int, question: QuestionMessage, answeredCorrectly: Boolean)
{
    override def toString() = "PlayerMessage { userId: " + userId + ", state: " + state + " x: " + x + ", y: " + y + ", question: " + question + ", answeredCorrectly:  " + answeredCorrectly + " }"
}

case class GameInfoResponse(override val gameId: Int, players: List[PlayerMessage], board: Array[Int]) extends GameRequestMessage
{
    override def toString() = "GameInfoResponse {gameId: " + gameId + ", players: (" + players.mkString(", ") + "), board: (" + board.mkString(", ") + ")}"
}

case class CreateGame(players: Array[Int]) extends GameRequestMessage
{
    override def toString() = "CreateGame {players: (" + players.mkString(", ") + ")}"
}

case class GameError(description: String, code: Int, reply: GameInfoResponse) extends ReplyMessage
{
    override def toString() = "GameError {what: " + description + ", code: " + code + ", gameinforeply: " + (if(reply == null) "none" else reply) + "}"
}

case class PlayerMove(override val gameId: Int, override val userId: Int, x: Int, y: Int) extends PlayerRequestMessage
{
    override def toString() = "PlayerMove {id: " + gameId + ", userId: " + userId + ", x: " + x + ", y: " + y + "}"
}
    
case class QuestionRequest(override val gameId: Int, override val userId: Int) extends PlayerRequestMessage
{
    override def toString() = "QuestionRequest { gameId: " + gameId + ", userId: " + userId + "}"
}
    
case class QuestionResponse(question: String, alternatives: List[String]) extends ReplyMessage
{
    override def toString() = "QuestionResponse { question: " + question + ", alternatives: (" + alternatives.mkString(", ") +  ") }"
}

case class Answer(override val gameId: Int, override val userId: Int, answer: Int) extends PlayerRequestMessage
{
    override def toString() = "AnswerRequest { gameId: " + gameId + ", userId: " + userId + ", answer: " + answer + "}" 
}

case class AnswerResponse(correctAnswer: Boolean) extends ReplyMessage
{
    override def toString() = "AnswerResponse { correctAnswer: " + correctAnswer + "}"
}