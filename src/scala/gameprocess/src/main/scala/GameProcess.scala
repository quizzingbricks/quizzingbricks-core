import akka.actor._
import akka.zeromq._
import akka.util.ByteString
import org.zeromq._
import scala.slick.driver.PostgresDriver.simple._

/**
 * The messaging broker main loop and entry point of the game process.
 */
object GameProcess
{
    def main(args: Array[String]) 
    {
        val back = 0; val front = 1
        
        val system = ActorSystem("zmq")
        val context = ZMQ.context(1)

        val backend  = context.socket(ZMQ.ROUTER)
        val frontend = context.socket(ZMQ.ROUTER)
        
        backend.bind("tcp://*:1235")
        frontend.bind("tcp://*:1234")

        val items = context.poller(2)
        
        items.register(backend, ZMQ.Poller.POLLIN)
        items.register(frontend, ZMQ.Poller.POLLIN) 
        
        val workerQ = scala.collection.mutable.Queue[Array[Byte]]()
        
        val gameCache = system.actorOf(Props(classOf[GameCache]))
        
        val db = Database.forURL("jdbc:postgresql://localhost:5432/quizzingbricks_dev",
                                 driver = "org.postgresql.Driver", user = "qb", password = "qb123")
        
        for (i <- 0 to 9)
        {
            system.actorOf(Props(classOf[BrokerWorker], i, gameCache))
        }    

        // Main message loop
        while (true) 
        {
            // Blocking poll until we receive a message
            items.poll
            if(items.pollin(back)) 
            {
                // The message format from the back is:
                // worker hash address | 0 | client hash address | message | message | ...
              
                println("Backend received a message!")
                val workerAddr = backend.recv(0)
                assert(backend.hasReceiveMore())
                val nil = backend.recv(0)
                assert(new String(nil) == "" && backend.hasReceiveMore())
                val clientAddr = backend.recv(0)
                
                if(backend.hasReceiveMore())
                {
                    val nil = backend.recv(0)
                    assert(new String(nil) == "" && backend.hasReceiveMore())
                    // Pass on the message to the client, the message now is:
                    // client hash address | 0 | message | message | ...
                    frontend.send(clientAddr, ZMQ.SNDMORE)
                    frontend.send("".getBytes, ZMQ.SNDMORE)
                    println("Sent to frontend!")
                    do
                    {
                        var msg = backend.recv(0)
                        frontend.send(msg, if (backend.hasReceiveMore) ZMQ.SNDMORE else 0)
                    } while (backend.hasReceiveMore())
                }
                else
                {
                    assert(new String(clientAddr) == "READY")
                    println("Received ready!")
                }
                // Enqueue the worker hash address for use in the next if statement                
                workerQ.enqueue(workerAddr)
            }
            if(items.pollin(front) && !workerQ.isEmpty)
            {
                // The message format from the front is:
                // client hash address | 0 | message | message | ...
                println("Frontend received a message")
                val clientAddr = frontend.recv(0)
                assert(frontend.hasReceiveMore())
                val nil = frontend.recv(0)
                assert(frontend.hasReceiveMore() && new String(nil) == "")

                // We dequeue a worker and use its address to construct a new message like this:
                // worker hash address | 0 | client hash address | 0 | message | message | ...
                backend.send(workerQ.dequeue, ZMQ.SNDMORE)
                backend.send("".getBytes, ZMQ.SNDMORE)
                backend.send(clientAddr, ZMQ.SNDMORE)
                //backend.send("".getBytes, ZMQ.SNDMORE)
                println("Sent to backend!")                
                do
                {
                    var msg = frontend.recv(0)
                    backend.send(msg, if (frontend.hasReceiveMore) ZMQ.SNDMORE else 0)
                } while (frontend.hasReceiveMore())
            }
        }
    }
}