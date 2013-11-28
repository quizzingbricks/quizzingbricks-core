

var BOARD_HEIGHT = 8
var BOARD_WIDTH  = 8
var last_marked_element =null;

var TOKEN = {
    EMPTY  : {value: 0, string: "Empty",    userId: 0 },
    RED    : {value: 1, string: "Red",      userId: -1 },
    YELLOW : {value: 2, string: "Yellow",   userId: -1 },
    BLUE   : {value: 3, string: "Blue",     userId: -1 },
    GREEN  : {value: 4, string: "Green",    userId: -1 }
}





var selected_token=TOKEN.RED;

/*function selectToken(token){
    document.getElementById('player_color').innerHTML = token.string;
    selected_token = token;
    
    $.post($SCRIPT_ROOT + '/choose_color', { token : token.string },
    function(data) {
    $("#resultColor").text(data.result);
    });
  }*/

function test_userId(token){ 
    alert(token.userId)
    //get_token_by_id(token.userId);
}


function assign_colors(friends, userId,gameId) {
    selected_token.userId = userId
    var length = friends.length,
    element = null;
    teststring = ""
    for (var i = 0; i < length; i++) {
        element = friends[i]; 
        teststring = teststring + element + " i: "+ i + "\n";
        if (i==0) { TOKEN.YELLOW.userId = element }
        if (i==1) { TOKEN.BLUE.userId   = element }
        if (i==2) { TOKEN.GREEN.userId  = element }
    }
    drawBoard(gameId);                                   //since it should be done onload but after assign_colors.
//alert(teststring);
}



function create_token(token, isConfirmed) {

    token_img = document.createElement("img");
    token_img.setAttribute("height", "64");
    token_img.setAttribute("width", "64");
    token_img.setAttribute("src", "/static/img/BoardCell_" + token.string + ".png");
    if (! isConfirmed){
        token_img.style.opacity="0.4";
    }
    
    return token_img        
}

var board = new Array(BOARD_HEIGHT)
for (var i = 0; i < board.length; i++) {
    board[i] = new Array(BOARD_WIDTH)
}

function updateStatus(players){
    var length = players.length
    element= null;
    for (var i = 0; i < length; i++) {
        element = players[i];
        if(element.state == 0 ){
            $("#status_id_"+element.userId).text("State: Placing Tile      ");
        }
        if(element.state == 1 ){
            $("#status_id_"+element.userId).text("State: Placed Tile       ");
        }
        if(element.state == 2 ){
            $("#status_id_"+element.userId).text("State: Answering Question");
        }
        if(element.state == 3 ){
            $("#status_id_"+element.userId).text("State: Answered Question ");
        }
    }

}

function drawBoard(gameId){
    //playerPos = [] 
    $.post($SCRIPT_ROOT + '/game_info', {gameId: gameId},
    function(data) {
        playerPos = data.board
        updateStatus(data.players);
       // $("#drawResult").text(playerPos[1]);
        for (var y =0; y<BOARD_HEIGHT; y++ ){
            for (var x=0; x<BOARD_WIDTH; x++){
                board_element = document.getElementById("square_"+ x+"_"+y);
                index = y*BOARD_HEIGHT +x;



                if(TOKEN.RED.userId == playerPos[index]){
                    board_element.innerHTML = ""
                    board_element.appendChild(create_token(TOKEN.RED,true));
                }
                else if(TOKEN.YELLOW.userId == playerPos[index]){
                    board_element.innerHTML = ""
                    board_element.appendChild(create_token(TOKEN.YELLOW,true));
                    //board_element.innerHTML = create_token(TOKEN.YELLOW).toString();
                }
                else if(TOKEN.BLUE.userId == playerPos[index]){
                    board_element.innerHTML = ""
                    board_element.appendChild(create_token(TOKEN.BLUE,true));
                    //board_element.innerHTML = create_token(TOKEN.BLUE);
                }
                else if(TOKEN.GREEN.userId == playerPos[index]){
                    board_element.innerHTML = ""
                    board_element.appendChild(create_token(TOKEN.GREEN,true));
                    //board_element.innerHTML = create_token(TOKEN.GREEN);
                }
                else if(board_element==last_marked_element){

                }
                else{
                    board_element.innerHTML = ""
                }
            }
        }
   //playerPos = data.board
   //$('#result').text(playerPos[1]);
  });
  //  board_element = document.getElementById("square_"+ 2+"_"+2);
  //  board_element.appendChild(create_token(TOKEN.RED));
  //  $('#result').text(playerPos[1]);
  // TODO: fetch playerPos for the board placements from the data object returned from Jquery call above
    //playerPos = [1,2,0,1,2]
    

}

function getQuestion(gameId){
        $.post($SCRIPT_ROOT + '/get_question', {gameId: gameId},
        function(data) {
            if (data.isQuestion){
                 $("#modalQuestion").text(data.question);
                 $("#question_alt_1").text(data.alternatives[0]);
                 $("#question_alt_2").text(data.alternatives[1]);
                 $("#question_alt_3").text(data.alternatives[2]);
                 $("#question_alt_4").text(data.alternatives[3]);
                 $('#myModal').modal('show')
            }

  }); 
}

function submitAnswer(gameId, answer){
    $.post($SCRIPT_ROOT + '/submit_answer', {gameId: gameId, answer: answer},
    function(data) {
        if(data.isCorrect){
            $("#answer").text("Correct answer");
        }
        else{
            $("#answer").text("Wrong answer");
        }
        last_marked_element=null;
        $('#myModal').modal('hide')
       // drawBoard(gameId);  
  }); 
}


function addTokens(gameId,x,y) {            //Send  gameId, x and y coordinates to run_web
 /*   player_color    = document.getElementById('player_color').innerHTML;
    board_element   = document.getElementById("square_" + x + "_" + y);    
    
    if (board[x][y] == null && selected_token != null) {
        board[x][y] = selected_token;

        board_element.appendChild(create_token(selected_token));*/
        
        $.post($SCRIPT_ROOT + '/make_move', {gameId: gameId, x: x, y: y },
        function(data) {
        $("#result").text(data.result);
        if(data.result=="Move sent"){

            board_element = document.getElementById("square_"+ x+"_"+y);
            board_element.appendChild(create_token(TOKEN.RED,false));
            last_marked_element=board_element
        }
      });
        
  //  }
}

var QuizzingBricks = QuizzingBricks || {};

QuizzingBricks.GameBoard = function(server_url, game_id) {
    // "fields"
    this.server_url = server_url;
    this.game_id = game_id;

    this._setup_websocket_listener = function() {
        if (window.WebSocket == undefined) {
            console.log("Websockets is not available in your browser");
        }
        var ws = new WebSocket("ws://" + this.server_url + "/api/games/" + this.game_id + "/events/");
        ws.onmessage = this._onReceiveEvent;
        ws.onerror = this._onSocketError;
        ws.onclose = this._onSocketClose;
    }


    this._onReceiveEvent = function(event) {
        // event = {"type": x, "payload": {} }
        console.log(event.data);
    }

    this._onSocketError = function(error) {
        console.log(error);
    }

    this._onSocketClose = function(e) {
        console.log("socket closed");
    }

    this.init = function() {
        // setup eventlisteners
        this._setup_websocket_listener();
    }
};
