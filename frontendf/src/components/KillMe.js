import React from 'react';
import ReactDOM from 'react-dom/client';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'

class KillMe extends React.Component {

    render() {
        return(
            
            <li>{this.props.name}</li>
        );
    }
}

export default KillMe;