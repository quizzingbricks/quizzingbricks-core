abstract class Message
{
}

abstract class GameRequestMessage extends Message
{
    var id: Int = 0
}

abstract class ReplyMessage extends Message
{
}

case class GameInfoRequest (theid: Int) extends GameRequestMessage
{
    id = theid
    override def toString() =
    {
        "GameInfoRequest {id: " + id + "}"
    }
}

case class GameInfoResponse (theid: Int, players: Array[Int], board: Array[Int]) extends GameRequestMessage
{
    id = theid
    override def toString() =
    {
        "GameInfoResponse {id: " + id + ", players: (" + players.mkString(", ") + "), board: (" + board.mkString(", ") + ")}" 
    }
}

case class CreateGame (players: Array[Int]) extends GameRequestMessage
{
    override def toString() =
    {
        "CreateGame {players: (" + players.mkString(", ") + ")}"
    }
}

case class GameError (description: String, code: Int, reply: GameInfoResponse) extends ReplyMessage
{
    override def toString() =
    {
        "GameError {what: " + description + ", code: " + code + ", gameinforeply: " + (if(reply == null) "none" else reply) + "}"
    }
}

case class PlayerMove (gameId: Int, userId: Int, x: Int, y: Int) extends GameRequestMessage
{
    id = gameId
    override def toString() =
    {
        "PlayerMove {id: " + gameId + ", userId: " + userId + ", x: " + x + ", y: " + y + "}"
    }
}