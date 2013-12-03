import akka.util.ByteString

/**
 * Static object acting as the translator between Protobuf and the internal case class representation. 
 */
object MessageTranslator
{
    val GAMEINFOREQUEST = 11
    val GAMEINFORESPONSE = 12
    val CREATEGAMEREQUEST = 10
    val CREATEGAMERESPONSE = 36
    val MOVEREQUEST = 13
    val MOVERESPONSE = 35
    val GAMEERROR = 14
    val QUESTIONREQUEST = 31
    val QUESTIONRESPONSE = 32
    val ANSWERREQUEST = 33
    val ANSWERRESPONSE = 34
    val GAMELISTREQUEST = 41
    val GAMELISTRESPONSE = 42
    
    val PLAYERSTATECHANGEPUBSUBMESSAGE = 70
    val NEWROUNDPUBSUBMESSAGE = 71
    
    /**
     * Transforms a Java list to a Scala list.
     * @param l The list to transform.
     */
    def javaListToList [A](l: java.util.List[A]): List[A] =
    {
        var ret: List[A] = Nil
        for(i <- 0 to l.size()-1)
            ret = ret ++ List[A](l.get(i))
        ret
    }
    
    /**
     * Transforms a Java list of Protobuf Player messages to a Scala list of player messages.
     * @param l The list of Player messages to translate. 
     */
    def playerMsgListToPlayerList (l: java.util.List[Gameprotocol.Player]) : List[PlayerMessage]=
    {
        var ret: List[PlayerMessage] = List[PlayerMessage]()
        for (i <- 0 to l.size()-1)
        { 
            var p = new PlayerMessage(l.get(i).getUserId(), l.get(i).getState(), l.get(i).getX(), 
                                      l.get(i).getY(), l.get(i).getQuestion(), 
                                      javaListToList(l.get(i).getAlternativesList()), l.get(i).getAnsweredCorrectly(),
                                      l.get(i).getScore())

            ret = ret ++ List[PlayerMessage](p)
        }
        ret
    }
    
    /**
     * Transforms a Java list of Protobuf Game messages to a Scala list of game messages.
     * @param l The list of Game messages to translate. 
     */
    def gameMsgArrayToGameList (l: java.util.List[Gameprotocol.Game]) : List[GameMessage] = 
    {
        var ret: List[GameMessage] = List[GameMessage]()
        
        for (i <- 0 to l.size()-1)
        {
            val protGame = l.get(i)
            
            var p = new GameMessage(protGame.getGameId(), playerMsgListToPlayerList(protGame.getPlayersList()), 
                                    javaListToList(protGame.getBoardList()).map(a => a.toInt).toArray)
            ret = ret ++ List[GameMessage](p)
        }
        ret
    }
    
    
    def buildGameMessage(m: GameMessage) =
    {
        var gameBuilder = Gameprotocol.Game.newBuilder()
        gameBuilder = gameBuilder.setGameId(m.gameId)
        for(b <- m.board)
            gameBuilder = gameBuilder.addBoard(b)
        for(p <- m.players)
        {
            var playerBuilder = Gameprotocol.Player.newBuilder()
            playerBuilder = playerBuilder.setUserId(p.userId).setState(p.state).setX(p.x).setY(p.y)
                                         .setAnsweredCorrectly(p.answeredCorrectly)
                                         .setQuestion(p.question).clearAlternatives().setScore(p.score)
            for(a <- p.alternatives)
            {
                playerBuilder = playerBuilder.addAlternatives(a)
            }
            gameBuilder = gameBuilder.addPlayers(playerBuilder.build())
        }
        gameBuilder.build()
    }
    
    /**
     * Translates a Protobuf message to an internal case class Message.
     * @param typ Integer conveying the message type of the bytestring to translate.
     * @param msgByteString The the message to translate.
     * @return The case class message representing the translated message.
     */
    def translate (typ: Int, msgByteString: ByteString): Message = 
    {
        typ match 
        {
            case GAMEINFOREQUEST =>
                val info = Gameprotocol.GameInfoRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                GameInfoRequest(info.getGameId())
            case GAMEINFORESPONSE =>
                val info = Gameprotocol.GameInfoResponse.newBuilder().mergeFrom(msgByteString.toArray).build()                
                GameInfoResponse(GameMessage(info.getGame().getGameId(), 
                                             playerMsgListToPlayerList(info.getGame().getPlayersList()), 
                                             javaListToList(info.getGame().getBoardList()).map(a => a.toInt).toArray))
            case CREATEGAMEREQUEST =>
                val createGameRequest = Gameprotocol.CreateGameRequest.newBuilder()
                                                    .mergeFrom(msgByteString.toArray).build()
                CreateGameRequest(javaListToList(createGameRequest.getPlayersList()).map(_.toInt))
            case CREATEGAMERESPONSE =>
                val createGameResponse = Gameprotocol.CreateGameResponse.newBuilder()
                                                     .mergeFrom(msgByteString.toArray).build()
                CreateGameResponse(createGameResponse.getGameId())
            case GAMEERROR =>
                val fail = Gameprotocol.GameError.newBuilder().mergeFrom(msgByteString.toArray).build()
                val info = fail.getGameinforeply()
                GameError(fail.getDescription(), fail.getCode())
            case MOVEREQUEST =>
                val info = Gameprotocol.MoveRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                MoveRequest(info.getGameId(), info.getUserId(), info.getX(), info.getY())
            case MOVERESPONSE =>
                MoveResponse()
            case QUESTIONREQUEST =>
                val qrq = Gameprotocol.QuestionRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                QuestionRequest(qrq.getGameId(), qrq.getUserId())
            case QUESTIONRESPONSE =>
                val qrs = Gameprotocol.QuestionResponse.newBuilder().mergeFrom(msgByteString.toArray).build()
                QuestionResponse(qrs.getQuestion(), javaListToList(qrs.getAlternativesList()))
            case ANSWERREQUEST =>
                val answer = Gameprotocol.AnswerRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                AnswerRequest(answer.getGameId(), answer.getUserId(), answer.getAnswer())
            case ANSWERRESPONSE =>
                val ar = Gameprotocol.AnswerResponse.newBuilder().mergeFrom(msgByteString.toArray).build()
                AnswerResponse(ar.getIsCorrect())
            case GAMELISTREQUEST =>
                val gameListRequest = Gameprotocol.GameListRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                GameListRequest(gameListRequest.getUserId())
            case GAMELISTRESPONSE =>
                val gameListResponse = Gameprotocol.GameListResponse.newBuilder()
                                                   .mergeFrom(msgByteString.toArray).build()
                GameListResponse(gameMsgArrayToGameList(gameListResponse.getGamesList()))
            case NEWROUNDPUBSUBMESSAGE =>
                val newRoundPubSubMessage = Gameprotocol.NewRoundPubSubMessage.newBuilder().mergeFrom(msgByteString.toArray).build()
                NewRoundPubSubMessage(GameMessage(newRoundPubSubMessage.getGame().getGameId(), 
                                             playerMsgListToPlayerList(newRoundPubSubMessage.getGame().getPlayersList()), 
                                             javaListToList(newRoundPubSubMessage.getGame().getBoardList()).map(a => a.toInt).toArray))
            case PLAYERSTATECHANGEPUBSUBMESSAGE =>
                val p = Gameprotocol.PlayerStateChangePubSubMessage.newBuilder().mergeFrom(msgByteString.toArray).build().getPlayer()
                PlayerStateChangePubSubMessage(PlayerMessage(p.getUserId(), p.getState(), p.getX(), 
                                      p.getY(), p.getQuestion(), 
                                      javaListToList(p.getAlternativesList()), p.getAnsweredCorrectly(),
                                      p.getScore()))
        }
    }
    
    /**
     * Translates a case class message to a Protobuf message.
     * @param message The case class of the message to translate.
     * @param msgByteString A pair where the first part is the message type as an integer and the second part
     *                      is the Protobuf string.
     */
    def translate (m: Message): (Int, ByteString) =
    {
        val ret = m match {
            case GameInfoRequest (id: Int) =>
                var gameInfoRequestBuilder = Gameprotocol.GameInfoRequest.newBuilder()
                gameInfoRequestBuilder.setGameId(id)
                (GAMEINFOREQUEST, gameInfoRequestBuilder.setGameId(id).build())
            case GameInfoResponse (m: GameMessage) =>
                var gameInfoResponseBuilder = Gameprotocol.GameInfoResponse.newBuilder()
                (GAMEINFORESPONSE, gameInfoResponseBuilder.setGame(buildGameMessage(m)).build())
            case CreateGameRequest (players: List[Int]) =>
                var createGameBuilder = Gameprotocol.CreateGameRequest.newBuilder()
                for (p <- players)
                    createGameBuilder = createGameBuilder.addPlayers(p)
                (CREATEGAMEREQUEST, createGameBuilder.build())
                
            case CreateGameResponse (gameId: Int) =>
                var createGameBuilder = Gameprotocol.CreateGameResponse.newBuilder().setGameId(gameId)
                (CREATEGAMERESPONSE, createGameBuilder.build())                
                
            case MoveRequest (gameId: Int, userId: Int, x: Int, y: Int) =>
                (MOVEREQUEST, Gameprotocol.MoveRequest.newBuilder().setGameId(gameId)
                                          .setUserId(userId).setX(x).setY(y).build())
                
            case MoveResponse () =>
                (MOVERESPONSE, Gameprotocol.MoveResponse.newBuilder().build())
            case GameError (what: String, code: Int) =>
                var builder = Gameprotocol.GameError.newBuilder().setDescription(what).setCode(code)
                (GAMEERROR, builder.build())                
            case QuestionRequest (gameId: Int, userId: Int) =>
                var builder = Gameprotocol.QuestionRequest.newBuilder().setGameId(gameId).setUserId(userId)
                (QUESTIONREQUEST, builder.build())
            case QuestionResponse (question: String, alternatives: List[String]) =>
                var builder = Gameprotocol.QuestionResponse.newBuilder().setQuestion(question)
                for(a <- alternatives)
                    builder = builder.addAlternatives(a)
                (QUESTIONRESPONSE, builder.build())
            case AnswerRequest (gameId: Int, userId: Int, answer: Int) =>
                var builder = Gameprotocol.AnswerRequest.newBuilder().setGameId(gameId)
                                                        .setUserId(userId).setAnswer(answer)
                (ANSWERREQUEST, builder.build())
            case AnswerResponse (isCorrect: Boolean) =>
                var builder = Gameprotocol.AnswerResponse.newBuilder().setIsCorrect(isCorrect)
                (ANSWERRESPONSE, builder.build())
            case GameListRequest (userId: Int) =>
                var builder = Gameprotocol.GameListRequest.newBuilder().setUserId(userId)
                (GAMELISTREQUEST, builder.build())
            case GameListResponse (games: List[GameMessage]) =>
                var gameListResponseBuilder = Gameprotocol.GameListResponse.newBuilder()
                for(game <- games)
                    gameListResponseBuilder.addGames(buildGameMessage(game))
                (GAMELISTRESPONSE, gameListResponseBuilder.build())
            case NewRoundPubSubMessage (m) =>
                var newRoundPubSubMessageBuilder = Gameprotocol.NewRoundPubSubMessage.newBuilder()
                (NEWROUNDPUBSUBMESSAGE, newRoundPubSubMessageBuilder.setGame(buildGameMessage(m)).build())
            case PlayerStateChangePubSubMessage (p) =>
                var playerStateChangePubSubMessage = Gameprotocol.PlayerStateChangePubSubMessage.newBuilder()
                var playerBuilder = Gameprotocol.Player.newBuilder().setUserId(p.userId).setState(p.state).setX(p.x)
                                          .setY(p.y).setAnsweredCorrectly(p.answeredCorrectly).setQuestion(p.question)
                                          .clearAlternatives().setScore(p.score)
                (PLAYERSTATECHANGEPUBSUBMESSAGE, playerStateChangePubSubMessage.setPlayer(playerBuilder.build()).build())
        }
        ret match { case (x: Int, y: com.google.protobuf.GeneratedMessage) => (x, ByteString(y.toByteArray())) }
    }
}