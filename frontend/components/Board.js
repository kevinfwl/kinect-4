import React from 'react';
import axios from 'axios';
import Cell from './cell';

const changeCell = (value) => {
    const identifierMap = {
        0: "blank_empty.png", 
        1: "blank_red.png", 
        2: "blank_yellow.png", 
        3: "red_empty.png", 
        4: "red_red.png", 
        5: "red_yellow.png", 
        6: "yellow_empty.png", 
        7: "yellow_red.png", 
        8: "yellow_yellow.png"
    }
    return identifierMap[value];
}

export default class Board extends React.Component {
    constructor() {
        super();
        var instance = axios.create({
            baseURL: 'https://6960384c.ngrok.io',
            timeout: 10000
        })
    }

    updateBoard() {
        axios.get('https://6960384c.ngrok.io/board/1')
        .then(function(response) {
            return response.data.arr.map((row) => {
                return row.map((elem) => {
                    return changeCell(elem);
                })
            });
        })
        .then(function(board) {
            return this.setStte({
                board: board
            })
        })
    }


   
    render() {
        return (
        <div>
            <div className="pieces">{this.handleSidePieces}</div>
            {console.log(this.updateBoard())}
            {this.state.board.map(row => {
                return <div className="board">{row.map(cell => {
                    return <Cell status={cell}/>
                })}</div>
             })}
            <div className="pieces">piecesplaceholder</div>
        </div>
    
        )
    }
}