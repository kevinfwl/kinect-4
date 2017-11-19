import React from 'react';
import axios from 'axios';

export default class PlayerTurn extends React.Component {
    constructor() {
        super();
        var instance = axios.create({
            baseURL: 'https://6960384c.ngrok.io',
            timeout: 10000
        })
    }
    
    // whosTurn(gesture) {
    //     //get requst with negative one --?
    //     axios.get('/cursor/down')
    //     .then(updateBoard())

    //     if(gesture == 'down') {
    //         //get column # and add 
    //         //redo the entire state
    //         if(document.getElementsByClassName('player').style.border = "3px solid #f3c315") {
    //             return computer;
    //         } else if(document.getElementsByClassName('computer').style.border = "3px solid #f3c315") {
    //             return person;
    //         }
    //     }
    // }
   
    render() {
        return (
        <div className="container">    
            <div className="players">
                { <h3 className="player">Player</h3> /*id={this.state.whosTurn = person ? selectedP : null} */}
                <h3 className="computer" /*id={this.state.whosTurn = computer? selectedC : null}*/>Computer</h3>
            </div>
         </div>
        )
    }
}