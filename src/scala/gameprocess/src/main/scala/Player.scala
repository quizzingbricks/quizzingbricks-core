import akka.actor._

/**
 * Case class representing a question from the database.
 * @param question The question.
 * @param alternatives The alternatives.
 * @param correctAnswer The correct alternative.
 */
case class Question(question: String, alternatives: List[String], correctAnswer: Int)
{
    override def toString() = "Question { question: " + question + ", alternatives: " + 
                              alternatives.mkString(", ") + ", correctAnswer: " + correctAnswer + " }"
}

/**
 * Static variables of the player class.
 */
object Player
{
    val PLACING = 0
    val PLACED = 1
    val ANSWERING = 2
    val ANSWERED = 3

    def stateToString(x: Int) = x match
    {
        case Player.PLACING => "PLACING"
        case Player.PLACED => "PLACED"
        case Player.ANSWERING => "ANSWERING"
        case Player.ANSWERED => "ANSWERED"
        case _ => "INVALID STATE (BUG)"
            
    }
    
}

/**
 * Class representing a player in a game.
 * @param userId The user id of this player.
 * @param state The current state of the player in the game.
 */
class Player (var userId: Int, var state: Int) 
{
    /**
     * @return The information about this player as a Protobuf message represented as a case class.
     */
    def toMessage() : PlayerMessage =
    {
        PlayerMessage(userId, state, x, y, question.question, question.alternatives, 
                      answer == question.correctAnswer && state == Player.ANSWERED)
    }    
    
    /**
     * Resets the state of this player and the internal variables.
     * @param toState The state to reset to.
     */
    def resetTo(toState: Int) =
    {
        state = toState
        state match
        {
            case Player.PLACING =>
                x = 0
                y = 0
                question = Question("", List("", "", "", ""), 0)
                answer = 0
                pendingTimeout = null
            case Player.PLACED =>
                question = Question("", List("", "", "", ""), 0)
                answer = 0
                pendingTimeout = null
            case _ =>
        }
    }
    
    var x: Int = 0
    var y: Int = 0
    
    var question: Question = Question("", List("", "", "", ""), 0)
    var answer: Int = 0
    
    var pendingTimeout: Cancellable = null
    
    override def toString = "Player { userId: " + userId + " state: " + Player.stateToString(state) + 
                                    ", x: " + x + ", y: " + y + ", question: " + question + ", answer: " + answer + "}"
}