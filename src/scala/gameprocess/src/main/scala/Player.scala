import akka.actor._

object Player
{
    val PLACING = 0
    val PLACED = 1
    val ANSWERING = 2
    val ANSWERED = 3

}

class Player (var userId: Int, var state: Int) {
    
    def stateToString(x: Int) = x match
    {
        case Player.PLACING => "PLACING"
        case Player.PLACED => "PLACED"
        case Player.ANSWERING => "ANSWERING"
        case Player.ANSWERED => "ANSWERED"
            
    }
    
    def reset()
    {
        state = Player.PLACING
        x = 0
        y = 0
        question = Question("", List("", "", "", ""), 0)
        answer = 0
        
        pendingTimeout = null
    }
    
    var x: Int = 0
    var y: Int = 0
    
    var question: Question = Question("", List("", "", "", ""), 0)
    var answer: Int = 0
    
    var pendingTimeout: Cancellable = null
    
    override def toString = "Player { userId: " + userId + " state: " + stateToString(state) + ", x: " + x + ", y: " + y + ", question: " + question + ", answer: " + answer + "}"
}