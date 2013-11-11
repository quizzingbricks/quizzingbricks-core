import akka.util.ByteString

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
    
    def scalaListToArray (l: java.util.List[Integer]): Array[Int] =
    {
        var ret: Array[Int] = Array[Int]()
        for (i <- 0 to l.size()-1)
        {
            ret :+= l.get(i).intValue()
        }
        ret
    }
    
    def scalaListToList [A](l: java.util.List[A]): List[A] =
    {
        var ret: List[A] = Nil
        for(i <- 0 to l.size()-1)
            ret = ret ++ List[A](l.get(i))
        ret
    }
    
    def playerMsgArrayToPlayerList (l: java.util.List[Gameprotocol.Player]) : List[PlayerMessage]=
    {
        var ret: List[PlayerMessage] = List[PlayerMessage]()
        for (i <- 0 to l.size()-1)
        { 
            var p = new PlayerMessage(l.get(i).getUserId(), l.get(i).getState(), l.get(i).getX(), l.get(i).getY(), l.get(i).getQuestion(), scalaListToList(l.get(i).getAlternativesList()), l.get(i).getAnsweredCorrectly())

            ret = ret ++ List[PlayerMessage](p)
        }
        ret
    }
    
    def translate (typ: Int, msgByteString: ByteString): Message = 
    {
        typ match 
        {
            case GAMEINFOREQUEST =>
                val info = Gameprotocol.GameInfoRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                GameInfoRequest(info.getGameId())
            case GAMEINFORESPONSE =>
                val info = Gameprotocol.GameInfoResponse.newBuilder().mergeFrom(msgByteString.toArray).build()
                GameInfoResponse(info.getGameId(), playerMsgArrayToPlayerList(info.getPlayersList()), scalaListToArray(info.getBoardList()))
            case CREATEGAMEREQUEST =>
                val createGameRequest = Gameprotocol.CreateGameRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                CreateGameRequest(scalaListToArray(createGameRequest.getPlayersList()))
            case CREATEGAMERESPONSE =>
                val createGameResponse = Gameprotocol.CreateGameResponse.newBuilder().mergeFrom(msgByteString.toArray).build()
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
                QuestionResponse(qrs.getQuestion(), List(""))
            case ANSWERREQUEST =>
                val answer = Gameprotocol.AnswerRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                AnswerRequest(answer.getGameId(), answer.getUserId(), answer.getAnswer())
            case ANSWERRESPONSE =>
                val ar = Gameprotocol.AnswerResponse.newBuilder().mergeFrom(msgByteString.toArray).build()
                AnswerResponse(ar.getIsCorrect())
        }
    }
    
    def translate (m: Message): (Int, ByteString) =
    {
        val ret = m match {
            case GameInfoRequest (id: Int) =>
                var gameInfoRequestBuilder = Gameprotocol.GameInfoRequest.newBuilder()
                gameInfoRequestBuilder.setGameId(id)
                (GAMEINFOREQUEST, Gameprotocol.GameInfoRequest.newBuilder().setGameId(id).build())
            case GameInfoResponse (id: Int, players: List[PlayerMessage], board: Array[Int]) =>
                var gameInfoReplyBuilder = Gameprotocol.GameInfoResponse.newBuilder()
                gameInfoReplyBuilder = gameInfoReplyBuilder.setGameId(id)
                for(b <- board)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addBoard(b)
                for(p <- players)
                {
                    var playerBuilder = Gameprotocol.Player.newBuilder()
                    playerBuilder = playerBuilder.setUserId(p.userId).setState(p.state).setX(p.x).setY(p.y).setAnsweredCorrectly(p.answeredCorrectly).setQuestion(p.question).clearAlternatives()
                    for(a <- p.alternatives)
                    {
                        playerBuilder = playerBuilder.addAlternatives(a)
                    }
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addPlayers(playerBuilder.build())
                }
                (GAMEINFORESPONSE, gameInfoReplyBuilder.build())
            case CreateGameRequest (players: Array[Int]) =>
                var createGameBuilder = Gameprotocol.CreateGameRequest.newBuilder()
                for (p <- players)
                    createGameBuilder = createGameBuilder.addPlayers(p)
                (CREATEGAMEREQUEST, createGameBuilder.build())
                
            case CreateGameResponse (gameId: Int) =>
                var createGameBuilder = Gameprotocol.CreateGameResponse.newBuilder().setGameId(gameId)
                (CREATEGAMERESPONSE, createGameBuilder.build())                
                
            case MoveRequest (gameId: Int, userId: Int, x: Int, y: Int) =>
                (MOVEREQUEST, Gameprotocol.MoveRequest.newBuilder().setGameId(gameId).setUserId(userId).setX(x).setY(y).build())
                
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
                var builder = Gameprotocol.AnswerRequest.newBuilder().setGameId(gameId).setUserId(userId).setAnswer(answer)
                (ANSWERREQUEST, builder.build())
            case AnswerResponse (isCorrect: Boolean) =>
                var builder = Gameprotocol.AnswerResponse.newBuilder().setIsCorrect(isCorrect)
                (ANSWERRESPONSE, builder.build())
        }
        ret match { case (x: Int, y: com.google.protobuf.GeneratedMessage) => (x, ByteString(y.toByteArray())) }
    }
}