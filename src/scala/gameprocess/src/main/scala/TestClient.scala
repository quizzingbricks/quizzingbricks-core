import org.zeromq.ZMQ
import org.zeromq.ZeroMQ
import akka.util.ByteString

object TestClient
{    
  def makeMessageFromString(n: Int, str: String): Message =
  {
      val args = str split(" ")
      n match {
          case 1 => 
              GameInfoRequest(args(0).toInt)
          case 2 =>
              CreateGame(args map(_.toInt))
          case 3 =>
              PlayerMove(args(0).toInt, args(1).toInt, args(2).toInt, args(3).toInt)
      }
  }
  
  def main(args : Array[String]) = {
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
      println("Choose message type:\n1: GameInfoRequest (id)\n2:CreateGame (players)\n3:PlayerMove (gameid player x y)")
      val n = readLine.toInt
      println("Arguments: ")
      var (x, msg) = MessageTranslator.translate(makeMessageFromString(n, readLine))
      socket.send(Array[Byte](x.toByte), ZMQ.SNDMORE)
      socket.send(msg.toArray, 0)
      println("Sent, waiting for reply...")
      val replyId = socket.recv(0)
      val reply = socket.recv(0)
      val rep = MessageTranslator.translate(replyId(0), ByteString(reply))
      //val msg2 = MessageTranslator.translate(rep)
      println("Reply received: " + rep)
      readLine
    }
  }
}