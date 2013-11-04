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

case class GameError (description: String, reply: GameInfoResponse) extends ReplyMessage
{
    override def toString() =
    {
        "GameError {what: " + description + ", gameinforeply: " + (if(reply == null) "none" else reply) + "}"
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