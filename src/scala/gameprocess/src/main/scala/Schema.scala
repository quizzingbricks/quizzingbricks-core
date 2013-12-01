import scala.slick.driver.PostgresDriver.simple._

/**
 * This table contains the board of each game. The board is in CSV form.
 */
object GamesTable extends Table[(Int, String)]("games") {
    def gameId = column[Int]("gameid", O.PrimaryKey, O.AutoInc)
    def board = column[String]("board")
    def autoInc = board returning gameId
    def * = gameId ~ board
}

/**
 * Junction table between games and their players.
 */
object PlayersGamesTable extends Table[(Int, Int, Int, Int, Int, String, String, String, 
                                        String, String, Int, Int)]("playersgames") {
    def playerId = column[Int]("playerid")
    def gameId = column[Int]("gameid")
    def state = column[Int]("state")
    def x = column[Int]("x")
    def y = column[Int]("y")
    def question = column[String]("question")
    def alt1 = column[String]("alt1")
    def alt2 = column[String]("alt2")
    def alt3 = column[String]("alt3")
    def alt4 = column[String]("alt4")
    def correctAnswer = column[Int]("correctanswer")
    def answer = column[Int]("answer")
    def * = playerId ~ gameId ~ state ~ x ~ y ~ question ~ alt1 ~ alt2 ~ alt3 ~ alt4 ~ correctAnswer ~ answer
    
    def pk = primaryKey("pk", (playerId, gameId))
    def idx1 = index("playeridx", (playerId, gameId), unique = true)
    def idx2 = index("gameidx", (gameId, playerId), unique = true)
}

/**
 * The questions table containing all the questions and their answers.
 */
object QuestionsTable extends Table[(Int, String, String, String, String, String, Int)]("questions") {
    def questionId = column[Int]("questionid", O.PrimaryKey, O.AutoInc)
    def question = column[String]("question")
    def alt1 = column[String]("alt1")
    def alt2 = column[String]("alt2")
    def alt3 = column[String]("alt3")
    def alt4 = column[String]("alt4")
    def answer = column[Int]("answer")
    def * = questionId ~ question ~ alt1 ~ alt2 ~ alt3 ~ alt4 ~ answer
}