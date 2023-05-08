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
	  modal_type: this.props.modal_type,
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
    if(this.state.modal_type === 0){
    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Player</ModalHeader>
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
	if(this.state.modal_type ===1){
		return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Todo Item</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="weapon-name">Weapon Name</Label>
              <Input
                type="text"
                id="weapon-name"
                name="weapon_name"
                defaultValue={this.state.activeItem.weapon_name}
				value={this.state.activeItem.weapon_name}
                onChange={this.handleChange}
                placeholder="Enter name"
              />
            </FormGroup>
            <FormGroup>
              <Label for="weapon-slot">Weapon Slot</Label>
              <Input
                type="text"
                id="weapon-slot"
                name="weapon_slot"
                defaultValue={this.state.activeItem.weapon_slot}
                onChange={this.handleChange}
                placeholder="Enter slot"
              />
            </FormGroup>
			<FormGroup>
              <Label for="weapon-element">Weapon Element</Label>
              <Input
                type="text"
                id="weapon-element"
                name="weapon_element"
                defaultValue={this.state.activeItem.weapon_element}
                onChange={this.handleChange}
                placeholder="0"
              />
            </FormGroup>
		    <FormGroup>
              <Label for="weapon-type">Weapon Type</Label>
              <Input
                type="text"
                id="weapon-type"
                name="weapon_type"
                defaultValue={this.state.activeItem.weapon_type}
                onChange={this.handleChange}
                placeholder="0"
              />
            </FormGroup>
		    <FormGroup>
              <Label for="weapon-damage">Weapon Damage</Label>
              <Input
                type="number"
                id="weapon-damage"
                name="weapon_damage"
                defaultValue={this.state.activeItem.weapon_damage}
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
	if(this.state.modal_type ===2){
		return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Location</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="location-name">Location Name</Label>
              <Input
                type="text"
                id="location-name"
                name="location_name"
                defaultValue={this.state.activeItem.location_name}
				value={this.state.activeItem.location_name}
                onChange={this.handleChange}
                placeholder="Enter name"
              />
            </FormGroup>
            <FormGroup>
              <Label for="enemy-type">Enemy Type</Label>
              <Input
                type="text"
                id="enemy-type"
                name="enemy_type"
                defaultValue={this.state.activeItem.enemy_type}
                onChange={this.handleChange}
                placeholder="Enter slot"
              />
            </FormGroup>
			<FormGroup>
              <Label for="min-level">Min Level</Label>
              <Input
                type="number"
                id="min-level"
                name="min_level"
                defaultValue={this.state.activeItem.min_level}
                onChange={this.handleChange}
                placeholder="0"
              />
            </FormGroup>
		    <FormGroup>
              <Label for="nr-public-events">Public Events</Label>
              <Input
                type="number"
                id="nr-public-events"
                name="nr_public_events"
                defaultValue={this.state.activeItem.nr_public_events}
                onChange={this.handleChange}
                placeholder="0"
              />
            </FormGroup>
		    <FormGroup>
              <Label for="nr-lost-sectors">Lost Sectors</Label>
              <Input
                type="number"
                id="nr-lost-sectors"
                name="nr_lost_sectors"
                defaultValue={this.state.activeItem.nr_lost_sectors}
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
	if(this.state.modal_type ===3){
		return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Login</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="username">Username</Label>
              <Input
                type="text"
                id="username"
                name="username"
                defaultValue={this.state.activeItem.username}
				value={this.state.activeItem.username}
                onChange={this.handleChange}
                placeholder="Enter username"
              />
            </FormGroup>
            <FormGroup>
              <Label for="password">Password</Label>
              <Input
                type="text"
                id="password"
                name="password"
                defaultValue={this.state.activeItem.password1}
                onChange={this.handleChange}
                placeholder="Enter slot"
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
}