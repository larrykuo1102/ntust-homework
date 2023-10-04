// 生成棋盤
function generateChessboard() {
    const queenCountInput = document.getElementById("queenCount");
    const queenPositionsInput = document.getElementById("queenPositions");
    const chessboard = document.getElementById("chessboard");

    // 獲取用戶輸入的皇后數量和位置
    const queenCount = parseInt(queenCountInput.value);
    const queenPositions = JSON.parse(queenPositionsInput.value);
    const gridSize = Math.ceil(Math.sqrt(queenCount));
    // 清空之前的棋盤
    chessboard.innerHTML = "";

    // 生成新的棋盤
    for (let row = 1; row <= queenCount; row++) {
        const rowDiv = document.createElement("div");
        rowDiv.className = "chessboard-row";

        for (let col = 1; col <= queenCount; col++) {
            const cell = document.createElement("div");
            cell.className = "cell";

            // 如果該位置有皇后，添加皇后樣式
            if (queenPositions.some(pos => pos[1] === row && pos[0] === col)) {
                const queenSymbol = document.createElement("span");
                queenSymbol.className = "queen";
                queenSymbol.textContent = "♛";
                cell.appendChild(queenSymbol);

            }

            rowDiv.appendChild(cell);
        }

        chessboard.appendChild(rowDiv);
    }

    // 顯示新生成的棋盤
    chessboard.style.display = "grid";
}

// 初始載入時生成一次棋盤
generateChessboard();
