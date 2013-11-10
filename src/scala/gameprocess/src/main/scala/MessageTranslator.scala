import akka.util.ByteString

object MessageTranslator
{
    val GAMEINFOREQUEST = 11
    val GAMEINFORESPONSE = 12
    val CREATEGAME = 10
    val PLAYERMOVE = 13
    val GAMEERROR = 14
    val QUESTIONREQUEST = 19
    val QUESTIONRESPONSE = 20
    val ANSWER = 21
    val ANSWERRESPONSE = 22
    
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
        { // userId: Int, state: Int, x: Int, y: Int, question: QuestionMessage, answeredCorrectly: Boolean
            var p = new PlayerMessage(l.get(i).getUserId(), l.get(i).getState(), l.get(i).getX(), l.get(i).getY(), QuestionMessage(l.get(i).getQuestion().getQuestion(), scalaListToList(l.get(i).getQuestion().getAlternativesList())), l.get(i).getAnsweredCorrectly())

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
                GameInfoRequest(info.getId())
            case GAMEINFORESPONSE =>
                val info = Gameprotocol.GameInfoResponse.newBuilder().mergeFrom(msgByteString.toArray).build()
                GameInfoResponse(info.getId(), playerMsgArrayToPlayerList(info.getPlayersList()), scalaListToArray(info.getBoardList()))
            case CREATEGAME =>
                val createGame = Gameprotocol.CreateGame.newBuilder().mergeFrom(msgByteString.toArray).build()
                CreateGame(scalaListToArray(createGame.getPlayersList()))
            case GAMEERROR =>
                val fail = Gameprotocol.GameError.newBuilder().mergeFrom(msgByteString.toArray).build()
                val info = fail.getGameinforeply()
                GameError(fail.getDescription(), fail.getCode(), GameInfoResponse(info.getId(), playerMsgArrayToPlayerList(info.getPlayersList()), scalaListToArray(info.getBoardList())))
            case PLAYERMOVE =>
                val info = Gameprotocol.PlayerMove.newBuilder().mergeFrom(msgByteString.toArray).build()
                PlayerMove(info.getGameId(), info.getUserId(), info.getX(), info.getY())
            case QUESTIONREQUEST =>
                val qrq = Gameprotocol.QuestionRequest.newBuilder().mergeFrom(msgByteString.toArray).build()
                QuestionRequest(qrq.getGameId(), qrq.getUserId())
            case QUESTIONRESPONSE =>
                val qrs = Gameprotocol.QuestionResponse.newBuilder().mergeFrom(msgByteString.toArray).build()
                QuestionResponse(qrs.getQuestion(), List(""))
            case ANSWER =>
                val answer = Gameprotocol.Answer.newBuilder().mergeFrom(msgByteString.toArray).build()
                Answer(answer.getGameId(), answer.getUserId(), answer.getAnswer())
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
                gameInfoRequestBuilder.setId(id)
                (GAMEINFOREQUEST, Gameprotocol.GameInfoRequest.newBuilder().setId(id).build())
            case GameInfoResponse (id: Int, players: List[PlayerMessage], board: Array[Int]) =>
                var gameInfoReplyBuilder = Gameprotocol.GameInfoResponse.newBuilder()
                gameInfoReplyBuilder = gameInfoReplyBuilder.setId(id)
                for(b <- board)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addBoard(b)
                var playerBuilder = Gameprotocol.Player.newBuilder()
                for(p <- players)
                {
                    var questionBuilder = Gameprotocol.Question.newBuilder().setQuestion(p.question.question)
                    for(a <- p.question.alternatives)
                    {
                        questionBuilder = questionBuilder.addAlternatives(a)
                    }
                    playerBuilder = playerBuilder.setUserId(p.userId).setState(p.state).setX(p.x).setY(p.y).setQuestion(questionBuilder.build).setAnsweredCorrectly(p.answeredCorrectly)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addPlayers(playerBuilder.build())
                }
                (GAMEINFORESPONSE, gameInfoReplyBuilder.build())
            case CreateGame (players: Array[Int]) =>
                var createGameBuilder = Gameprotocol.CreateGame.newBuilder()
                for (p <- players)
                    createGameBuilder = createGameBuilder.addPlayers(p)
                (CREATEGAME, createGameBuilder.build())
                
            case PlayerMove (gameId: Int, userId: Int, x: Int, y: Int) =>
                (PLAYERMOVE, Gameprotocol.PlayerMove.newBuilder().setGameId(gameId).setUserId(userId).setX(x).setY(y).build())
            case GameError (what: String, code: Int, null) =>
                var builder = Gameprotocol.GameError.newBuilder().setDescription(what).setCode(code)
                (GAMEERROR, builder.build())                
            case GameError (what: String, code: Int, info: GameInfoResponse) =>
                var builder = Gameprotocol.GameError.newBuilder().setDescription(what).setCode(code)
                var gameInfoReplyBuilder = Gameprotocol.GameInfoResponse.newBuilder()
                gameInfoReplyBuilder = gameInfoReplyBuilder.setId(info.gameId)
                for(b <- info.board)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addBoard(b)
                var playerBuilder = Gameprotocol.Player.newBuilder()
                for(p <- info.players)
                {
                    var questionBuilder = Gameprotocol.Question.newBuilder().setQuestion(p.question.question)
                    for(a <- p.question.alternatives)
                    {
                        questionBuilder = questionBuilder.addAlternatives(a)
                    }
                    playerBuilder = playerBuilder.setUserId(p.userId).setState(p.state).setX(p.x).setY(p.y).setQuestion(questionBuilder.build)
                    gameInfoReplyBuilder = gameInfoReplyBuilder.addPlayers(playerBuilder.build())
                }
                builder.setGameinforeply(gameInfoReplyBuilder.build())
                (GAMEERROR, builder.build())
            case QuestionRequest (gameId: Int, userId: Int) =>
                var builder = Gameprotocol.QuestionRequest.newBuilder().setGameId(gameId).setUserId(userId)
                (QUESTIONREQUEST, builder.build())
            case QuestionResponse (question: String, alternatives: List[String]) =>
                var builder = Gameprotocol.QuestionResponse.newBuilder().setQuestion(question)
                (QUESTIONRESPONSE, builder.build())
            case Answer (gameId: Int, userId: Int, answer: Int) =>
                var builder = Gameprotocol.Answer.newBuilder().setGameId(gameId).setUserId(userId).setAnswer(answer)
                (ANSWER, builder.build())
            case AnswerResponse (isCorrect: Boolean) =>
                var builder = Gameprotocol.AnswerResponse.newBuilder().setIsCorrect(isCorrect)
                (ANSWERRESPONSE, builder.build())
        }
        ret match { case (x: Int, y: com.google.protobuf.GeneratedMessage) => (x, ByteString(y.toByteArray())) }
    }
}