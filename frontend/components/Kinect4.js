import React from 'react';
import Header from './Header'
import Board from './Board'; //can skip js if inside webpack
import PlayerTurn from './PlayerTurn';

class Kinect4 extends React.Component {
    state = {
        options: [], 
        selectedOption: undefined //when the user first visits, no readon 
    };
 
    handleDeleteOptions = () => {
        this.setState(() => ({ options: [] }));
    }

    handleDeleteOption = (optionToRemove) => {
        this.setState((prevState) => ({
            options: prevState.options.filter((option) => optionToRemove !== option)
        }))
    }

    handlePick = () => {
        const randomNum = Math.floor(Math.random() * this.state.options.length);
        const option = this.state.options[randomNum];
        this.setState(() => ({ selectedOption: option }))
    }

    handleAddOption = (option) => {
        if(!option) {
            return 'Enter valid value to add item';
        } else if (this.state.options.indexOf(option) > -1) {
            return 'This option already exists';
        } 

        this.setState((prevState) => ({
            options: prevState.options.concat(option)
        }));
    }

    handleClearSelectedOption = () => {
        this.setState(() => ({ selectedOption: undefined }))
    }
    
    componentDidMount() {
        try {
            const json = localStorage.getItem('options');
            const options = JSON.parse(json);
            if(options) {
                this.setState(() => ({options}));        
            }
        } catch(e) {
            //DO NOTHING AT AL;
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if(prevState.options.length !== this.state.options.length) {
            const json = JSON.stringify(this.state.options);
            localStorage.setItem('options', json);           
        }
    }

    componentWillUnmount() {
        console.log('componentWillUnmount')
    }

    render() {
        const subtitle = "Put your pride in the hands of a computer";
        return (
            <div>
                <Header subtitle ={subtitle} />
                <div className="container">
                    <Board/>
                    <PlayerTurn />
                </div>
            </div>
        );
    }
}

export default Kinect4;