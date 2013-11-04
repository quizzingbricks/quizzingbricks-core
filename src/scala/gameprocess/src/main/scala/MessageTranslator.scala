import akka.util.ByteString

object MessageTranslator
{
    val GAMEINFOREQUEST = 11
    val GAMEINFORESPONSE = 12
    val CREATEGAME = 10
    val PLAYERMOVE = 13
    val GAMEERROR = 14
    
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
            case GAMEINFORESPONSE =>
                val info = Gameprotocol.GameInfoResponse.newBuilder().mergeFrom ( msgByteString.toArray ).build()
                GameInfoResponse(info.getId(), scalaListToArray(info.getPlayersList()), scalaListToArray(info.getBoardList()))
            case CREATEGAME =>
                val createGame = Gameprotocol.CreateGame.newBuilder().mergeFrom ( msgByteString.toArray ).build()
                CreateGame(scalaListToArray(createGame.getPlayersList()))
            case GAMEERROR =>
                val fail = Gameprotocol.GameError.newBuilder().mergeFrom ( msgByteString.toArray ).build()
                val info = fail.getGameinforeply()
                GameError(fail.getDescription(), GameInfoResponse(info.getId(), scalaListToArray(info.getPlayersList()), scalaListToArray(info.getBoardList())))
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
            case GameInfoResponse (id: Int, players: Array[Int], board: Array[Int]) =>
                var gameInfoReplyBuilder = Gameprotocol.GameInfoResponse.newBuilder()
                gameInfoReplyBuilder = gameInfoReplyBuilder.setId(id)
                for(b <- board)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addBoard(b)
                for(p <- players)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addPlayers(p)
                (GAMEINFORESPONSE, gameInfoReplyBuilder.build())
            case CreateGame (players: Array[Int]) =>
                var createGameBuilder = Gameprotocol.CreateGame.newBuilder()
                for (p <- players)
                    createGameBuilder = createGameBuilder.addPlayers(p)
                (CREATEGAME, createGameBuilder.build())
                
            case PlayerMove (gameId: Int, playerId: Int, x: Int, y: Int) =>
                (PLAYERMOVE, Gameprotocol.PlayerMove.newBuilder().setGameId(gameId).setPlayerId(playerId).setX(x).setY(y).build())
            case GameError (what: String, null) =>
                var builder = Gameprotocol.GameError.newBuilder().setDescription(what)
                (GAMEERROR, builder.build())                
            case GameError (what: String, info: GameInfoResponse) =>
                var builder = Gameprotocol.GameError.newBuilder().setDescription(what)
                var gameInfo : Gameprotocol.GameInfoResponse = null

                var gameInfoReplyBuilder = Gameprotocol.GameInfoResponse.newBuilder()
                gameInfoReplyBuilder = gameInfoReplyBuilder.setId(info.id)
                for(b <- info.board)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addBoard(b)
                for(p <- info.players)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addPlayers(p)
                gameInfo = gameInfoReplyBuilder.build()
                builder.setGameinforeply(gameInfo)

                (GAMEERROR, builder.build())
        }
        ret match { case (x: Int, y: com.google.protobuf.GeneratedMessage) => (x, ByteString(y.toByteArray())) }
    }
}