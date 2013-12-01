import org.zeromq.ZMQ
import org.zeromq.ZeroMQ
import akka.util.ByteString

object TestClient
{    
    def makeMessageFromString(n: Int, str: String): Message =
    {
        val args = str split(" ")
        n match
        {
            case 1 => 
                GameInfoRequest(args(0).toInt)
            case 2 =>
                CreateGameRequest(args.toList.map(_.toInt))
            case 3 =>
                MoveRequest(args(0).toInt, args(1).toInt, args(2).toInt, args(3).toInt)
            case 4 =>
                QuestionRequest(args(0).toInt, args(1).toInt)
            case 5 =>
                AnswerRequest(args(0).toInt, args(1).toInt, args(2).toInt)
            case 6 =>
                GameListRequest(args(0).toInt)
            case _ =>
                throw new Exception("Wrong argument!")
        }
    }
    
    def makeMsg(n: Int) : (Int, ByteString) =
    {
        try
        {
            MessageTranslator.translate(makeMessageFromString(n, readLine))
        }
        catch
        {
            case _ : IndexOutOfBoundsException =>
                println("Wrong number of parameters. Try again.")
                makeMsg(n)
            case _ : NumberFormatException =>
                println("Please input numbers only. Try again.")
                makeMsg(n)
        }
    }

    def readInt() : Int = 
    {
        try
        {
            while(true)
            {
                val n = readLine.toInt
                if (n < 0 || n > 6)
                {
                    println("0-6 only, try again!")
                    return readInt
                }
                else
                    return n
            }
            0 // this is retarded, in fact this whole file is
        }
        catch
        {
            case _ : java.lang.NumberFormatException => 
                println("Please input a number. Try again.")
                readInt
            case e : Exception =>
                print(e.getMessage() + " Try again!\n")
                readInt
        }
    }
    
    def main(args : Array[String]) = 
    {
        val context = ZMQ.context(1)
        val socket = context.socket(ZMQ.REQ)
        try socket.connect ("tcp://127.0.0.1:1234")
        catch
        {
            case e: Exception =>
                println("Couldn't connect to server!")
        }
        
           
        while( true )
        {
            println("Choose message type:\n1: GameInfoRequest (id)\n2: CreateGame (players)\n" +
            "3: PlayerMove (gameid player x y)\n4: QuestionRequest (gameid player) \n5: Answer (gameid player answer)\n6: GameListRequest(user id)")
            val n = readInt
            println("Arguments: ")
            val (x, msg) = makeMsg(n)
            socket.send(x.toString().getBytes, ZMQ.SNDMORE)
            socket.send(msg.toArray, 0)
            println("Sent, waiting for reply...")
            val replyId = socket.recv(0)
            val reply = socket.recv(0)
            val rep = MessageTranslator.translate(replyId.foldLeft("")((str, n) => str + n.toChar).toInt , ByteString(reply))
            //val msg2 = MessageTranslator.translate(rep)
            println("Reply received: " + rep)
        }
    }
}