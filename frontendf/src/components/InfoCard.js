import React from 'react';
import ReactDOM from 'react-dom/client';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'

class InfoCard extends React.Component {
    
    render() {
        return(
            <Card>   
                <Card.Body>
                    <Card.Title>{this.props.name}</Card.Title>
                    <Card.Text>{this.props.name}</Card.Text>
                    {console.log(this.props)}
                </Card.Body>
            </Card>
        );
    }
}

export default InfoCard;