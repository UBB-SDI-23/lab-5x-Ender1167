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

export default class CustomModal1 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeWeapon,
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
}