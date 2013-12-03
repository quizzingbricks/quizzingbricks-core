import akka.zeromq._
import akka.actor.Actor
import akka.actor.Props
 
/**
 * Class responsible for publishing ZMQ messages.
 */
class Publisher extends Actor
{
    val pubSocket = ZeroMQExtension(context.system).newSocket(SocketType.Pub, Connect("tcp://127.0.0.1:5201"))
    
    def receive: Receive = 
    {
        case m: ZMQMessage =>
            pubSocket ! m
        case _ =>
            println("Publisher received something weird!")
    }
}