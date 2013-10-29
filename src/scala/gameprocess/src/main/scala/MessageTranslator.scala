import akka.util.ByteString

object MessageTranslator
{
    val GAMEINFOREQUEST = 1
    val GAMEINFOREPLY = 11
    val CREATEGAME = 10
    val PLAYERMOVE = 4
    val FAILURE = 5
    
    def scalaListToArray (l: java.util.List[Integer]): Array[Int] =
    {
        var ret: Array[Int] = Array[Int]()
        for (i <- 0 to l.size()-1)
        {
            ret :+= l.get(i).intValue()
        }
        ret
    }
    
    def translate (typ: Int, msgByteString: ByteString): Message = 
    {
        typ match 
        {
            case GAMEINFOREQUEST =>
                val info = Gameprotocol.GameInfoRequest.newBuilder().mergeFrom( msgByteString.toArray ).build()
                GameInfoRequest(info.getId())
            case GAMEINFOREPLY =>
                val info = Gameprotocol.GameInfoReply.newBuilder().mergeFrom ( msgByteString.toArray ).build()
                GameInfoReply(info.getId(), scalaListToArray(info.getPlayersList()), scalaListToArray(info.getBoardList()))
            case CREATEGAME =>
                val createGame = Gameprotocol.CreateGame.newBuilder().mergeFrom ( msgByteString.toArray ).build()
                CreateGame(scalaListToArray(createGame.getPlayersList()))
            case FAILURE =>
                val fail = Gameprotocol.Failure.newBuilder().mergeFrom ( msgByteString.toArray ).build()
                Failure(fail.getWhat())
            case PLAYERMOVE =>
                val info = Gameprotocol.PlayerMove.newBuilder().mergeFrom ( msgByteString.toArray ).build()
                PlayerMove(info.getGameId(), info.getPlayerId(), info.getX(), info.getY())
        }
    }
    
    def translate (m: Message): (Int, ByteString) =
    {
        val ret = m match {
            case GameInfoRequest (id: Int) =>
                var gameInfoRequestBuilder = Gameprotocol.GameInfoRequest.newBuilder()
                gameInfoRequestBuilder.setId(id)
                (GAMEINFOREQUEST, Gameprotocol.GameInfoRequest.newBuilder().setId(id).build())
            case GameInfoReply (id: Int, players: Array[Int], board: Array[Int]) =>
                var gameInfoReplyBuilder = Gameprotocol.GameInfoReply.newBuilder()
                gameInfoReplyBuilder = gameInfoReplyBuilder.setId(id)
                for(b <- board)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addBoard(b)
                for(p <- players)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addPlayers(p)
                (GAMEINFOREPLY, gameInfoReplyBuilder.build())
            case CreateGame (players: Array[Int]) =>
                var createGameBuilder = Gameprotocol.CreateGame.newBuilder()
                for (p <- players)
                    createGameBuilder = createGameBuilder.addPlayers(p)
                (CREATEGAME, createGameBuilder.build())
                
            case PlayerMove (gameId: Int, playerId: Int, x: Int, y: Int) =>
                (PLAYERMOVE, Gameprotocol.PlayerMove.newBuilder().setGameId(gameId).setPlayerId(playerId).setX(x).setY(y).build())
            case Failure (what: String) =>
                (FAILURE, Gameprotocol.Failure.newBuilder().setWhat(what).build())
        }
        ret match { case (x: Int, y: com.google.protobuf.GeneratedMessage) => (x, ByteString(y.toByteArray())) }
    }
}