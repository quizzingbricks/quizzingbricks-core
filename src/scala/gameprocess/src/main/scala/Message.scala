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

case class GameInfoReply (theid: Int, players: Array[Int], board: Array[Int]) extends GameRequestMessage
{
    id = theid
    override def toString() =
    {
        "GameInfoReply {id: " + id + ", players: (" + players.mkString(", ") + "), board: (" + board.mkString(", ") + ")}" 
    }
}

case class CreateGame (players: Array[Int]) extends GameRequestMessage
{
    override def toString() =
    {
        "CreateGame {players: (" + players.mkString(", ") + ")}"
    }
}

case class Failure (what: String) extends ReplyMessage
{
    override def toString() =
    {
        "Failure {what: " + what + "}"
    }
}

case class PlayerMove (gameId: Int, playerId: Int, x: Int, y: Int) extends GameRequestMessage
{
    id = gameId
    override def toString() =
    {
        "PlayerMove {id: " + gameId + ", playerId: " + playerId + ", x: " + x + ", y: " + y + "}"
    }
}