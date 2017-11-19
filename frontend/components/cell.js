import React from 'react';

class Cell extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            status: this.props.state
        }
    }

    render() {
        return (
            <div>
                <tr></tr>
            </div>
        )
    }
}