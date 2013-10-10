var selected_token;

var BOARD_HEIGHT = 10
var BOARD_WIDTH  = 10

var TOKEN = {
    EMPTY  : {value: 0, string: "Empty"},
    RED    : {value: 1, string: "Red"},
    YELLOW : {value: 2, string: "Yellow"},
    BLUE   : {value: 3, string: "Blue"},
    GREEN  : {value: 4, string: "Green"}

}  

function selectToken(token){
    document.getElementById('player_color').innerHTML = token.string;
    selected_token = token;
    
    $.post($SCRIPT_ROOT + '/choose_color', { token : token.string },
    function(data) {
    $("#resultColor").text(data.result);
    });
  }


function create_token(token) {

    token_img = document.createElement("img");
    token_img.setAttribute("height", "64");
    token_img.setAttribute("width", "64");
    token_img.setAttribute("src", "static/img/BoardCell_" + token.string + ".png");
    
    return token_img        
}

var board = new Array(BOARD_HEIGHT)
for (var i = 0; i < board.length; i++) {
    board[i] = new Array(BOARD_WIDTH)
}

function addTokens(x,y) {
    player_color    = document.getElementById('player_color').innerHTML;
    board_element   = document.getElementById("square_" + x + "_" + y);    
    
    if (board[x][y] == null && selected_token != null) {
        board[x][y] = selected_token;

        board_element.appendChild(create_token(selected_token));
        
        $.post($SCRIPT_ROOT + '/game_board', { x: x, y: y },
        function(data) {
        $("#result").text(data.result);
      });
    }
}


