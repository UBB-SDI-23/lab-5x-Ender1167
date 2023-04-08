import React, { Component } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label,
} from "reactstrap";

export default class CustomModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
    };
  }

  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };

  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Todo Item</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="player-name">Name</Label>
              <Input
                type="text"
                id="player-name"
                name="name"
                defaultValue={this.state.activeItem.name}
				value={this.state.activeItem.name}
                onChange={this.handleChange}
                placeholder="Enter name"
              />
            </FormGroup>
            <FormGroup>
              <Label for="player-class">Class</Label>
              <Input
                type="text"
                id="player-class"
                name="class1"
                defaultValue={this.state.activeItem.class1}
                onChange={this.handleChange}
                placeholder="Enter class"
              />
            </FormGroup>
			<FormGroup>
              <Label for="player-level">Level</Label>
              <Input
                type="number"
                id="player-level"
                name="level"
                defaultValue={this.state.activeItem.level}
                onChange={this.handleChange}
                placeholder="0"
              />
            </FormGroup>
		    <FormGroup>
              <Label for="player-glimmer">Glimmer</Label>
              <Input
                type="number"
                id="player-glimmer"
                name="glimmer"
                defaultValue={this.state.activeItem.glimmer}
                onChange={this.handleChange}
                placeholder="0"
              />
            </FormGroup>
		    <FormGroup>
              <Label for="player-shards">Shards</Label>
              <Input
                type="number"
                id="player-shards"
                name="shards"
                defaultValue={this.state.activeItem.shards}
                onChange={this.handleChange}
                placeholder="0"
              />
            </FormGroup>
          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={() => onSave(this.state.activeItem)}
          >
            Save
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}