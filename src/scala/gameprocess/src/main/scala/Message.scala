/**
 * Abstract case class representing any network message.
 */
abstract class Message
{
}

/**
 * Abstract case class representing any incoming messages that are addressed to a specific game.
 */
abstract class GameRequestMessage extends Message
{
    val gameId: Int = 0
}

/**
 * Abstract case class representing any incoming messages that deal with a specific player in a specific game.
 */
abstract class PlayerRequestMessage extends GameRequestMessage
{
    val userId: Int = 0
}

/**
 * Outgoing messages.
 */
abstract class ReplyMessage extends Message
{
}

/**
 * Abstract case class representing the protocol for conveying information about a specific game.
 * @param gameId The id of the game.
 * @param players Information about the players in the game represented as a list of playermessages.
 * @param board Array of integers representing the game board. Each integer is the user id of the player who
 *              placed the brick on the position.
 */
case class GameMessage(gameId: Int, players: List[PlayerMessage], board: Array[Int]) extends ReplyMessage
{
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

/**
 * Case class representing the CreateGameRequest protocol message.
 * @param list The list of players that are going to participate in the game. 
 */
case class CreateGameRequest(players: List[Int]) extends GameRequestMessage
{
    override def toString() = "CreateGame {players: (" + players.mkString(", ") + ") }"
}

/**
 * Case class representing the CreateGameResponse message.
 * @param The id of the game that was created. 
 */
case class CreateGameResponse(gameId: Int) extends ReplyMessage
{
    override def toString() = "CreateGameResponse { gameId: " + gameId + " }"
}

/**
 * Case class representing the GameInfoRequest message.
 * @param gameId The id of the game whose information is being requested.
 */
case class GameInfoRequest(override val gameId: Int) extends GameRequestMessage
{
    override def toString() = "GameInfoRequest { gameId: " + gameId + " }"
}

/**
 * Case class representing the GameInfoResponse message, actually just a wrapper for a GameMessage.
 * @param game The GameMessage containing all the information.
 */
case class GameInfoResponse(game: GameMessage) extends ReplyMessage
{
    override def toString() = "GameInfoResponse { game: " + game + " }"
}

/**
 * Case class representing the GameListRequest message.
 * @param userId The id of the user whose games we want information of.
 */
case class GameListRequest(userId: Int) extends Message
{
    override def toString() = "GameListRequest { userId: " + userId + " }"
}

/**
 * Case class representing the GameListResponse message.
 * @param gameList Information about the games that the user is part of, as a list of GameMessages.
 */
case class GameListResponse(gameList: List[GameMessage]) extends ReplyMessage
{
    override def toString() = "GameListMessage { gameList: " + gameList.mkString(", ") + " }"
}

/**
 * Case class representing the PlayerMessage message, which contains information about a player in a game.
 * @param userId The id of the user.
 * @param state The current state of the player.
 * @param x The x coordinate of the prospected position of a possibly placed brick. Only applicable if state is
 *          PLACED, ANSWERING or ANSWERED.
 * @param y The y coordinate of the prospected position of a possibly placed brick. Only applicable if state is 
 *          PLACED, ANSWERING or ANSWERED.
 * @param question The question the player is possibly currently answering. Only applicable if state is
 *                 ANSWERING (or ANSWERED).
 * @param alternatives The list of answer alternatives for the current question. Only applicable if state is ANSWERING.
 * @param answeredCorrectly True if the player answered correctly, false if not. Only applicable if state is ANSWERED.                 
 */
case class PlayerMessage(userId: Int, state: Int, x: Int, y: Int, 
                         question: String, alternatives: List[String], answeredCorrectly: Boolean)
{
    override def toString() = "player " + userId + " [" + Player.stateToString(state) + "]: " + "(" + x + "," + y + 
                              ")\n question: " + question.take(20) + "[...]" + "\n  alternatives: " + 
                              alternatives.mkString + "\n  answeredCorrectly " + answeredCorrectly 
}

/**
 * Case class representing the MoveRequest message.
 * @param gameId Id of the game that the player wants to make a move in.
 * @param userId Id of the player who wants to make the move.
 * @param x The x coordinate of the move.
 * @param y The y coordinate of the move.
 */
case class MoveRequest(override val gameId: Int, override val userId: Int, x: Int, y: Int) extends PlayerRequestMessage
{
    override def toString() = "MoveRequest { id: " + gameId + ", userId: " + userId + ", x: " + x + ", y: " + y + " }"
}

/**
 * Case class representing the MoveResponse message.
 */
case class MoveResponse() extends ReplyMessage
{
    override def toString() = "MoveResponse { }"
}

/**
 * Case class representing the QuestionRequest message.
 * @param gameId The id of the recipient game.
 * @param userId The id of the user who wants the quest.n
 */
case class QuestionRequest(override val gameId: Int, override val userId: Int) extends PlayerRequestMessage
{
    override def toString() = "QuestionRequest { gameId: " + gameId + ", userId: " + userId + " }"
}

/**
 * Case class representing the QuestionResponse message.
 * @param question The question the player received.
 * @param alternatives The answer alternatives.
 */
case class QuestionResponse(question: String, alternatives: List[String]) extends ReplyMessage
{
    override def toString() = "QuestionResponse { question: " + question + ", alternatives: (" + 
                              alternatives.mkString(", ") +  ") }"
}

/**
 * Case class representing the AnswerRequest message.
 * @param gameId The id of the recipient game.
 * @param player The user id of the answerer.
 * @param answer The answer alternative.
 */
case class AnswerRequest(override val gameId: Int, override val userId: Int, answer: Int) extends PlayerRequestMessage
{
    override def toString() = "AnswerRequest { gameId: " + gameId + ", userId: " + userId + ", answer: " + answer + " }" 
}

/**
 * Case class representing the AnswerResponse message.
 * @param correctAnswer True if the answer is correct, false if not.
 */
case class AnswerResponse(correctAnswer: Boolean) extends ReplyMessage
{
    override def toString() = "AnswerResponse { correctAnswer: " + correctAnswer + " }"
}

/**
 * Case class representing the GameError message.
 * @param description The description of the error.
 * @param code The numerical error code.
 */
case class GameError(description: String, code: Int) extends ReplyMessage
{
    override def toString() = "GameError { what: " + description + ", code: " + code + " }"
}



    


