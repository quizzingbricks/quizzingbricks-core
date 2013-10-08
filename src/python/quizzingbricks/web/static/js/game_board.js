var selected_token;

var BOARD_HEIGHT = 8
var BOARD_WIDTH  = 8 

var TOKEN = {
    BLACK  : {value: 0, string: "Black"},
    WHITE  : {value: 1, string: "White"},
    RED    : {value: 2, string: "Red"},
    YELLOW : {value: 3, string: "Yellow"},
    BLUE   : {value: 4, string: "Blue"},
    GREEN  : {value: 5, string: "Green"},
    PINK   : {value: 6, string: "Pink"},
    TEAL   : {value: 7, string: "Teal"}
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
    token_img.setAttribute("height", "56");
    token_img.setAttribute("width", "56");
    token_img.setAttribute("src", "static/img/" + token.string + "_Token.png");
    
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


