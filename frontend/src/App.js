
import './App.css';
import Modal from "./components/Modal";
import React, { Component } from "react";
import axios from "axios";
import {
  FormGroup,
  Input,
  Label,
} from "reactstrap";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      viewCompleted: 1,
      players: [],
	  numDescending: [],
	  reportPlayers: [],
	  filterPlayers: [],
	  
	  pageNumbers: [],
	  totalItems: 1000000,
	  perPage: 10,
	  currentPage:1,
	  
	  locations: [],
	  weapons: [],
	  
	  filterValue: 0,
	  nextUrl:"",
	  previousUrl:"",
	  modal: false,
	  modal_weapon: false,
	  modal_location: false,
	  modal_login: false,
	  modal_type:0,
	  
      activeItem: {
        name: "",
        class1: "",
		level: 0,
		glimmer:0,
		shards:0,
      },
	  activeWeapon: {
        weapon_name: "",
        weapon_slot: "",
		weapon_element: "",
		weapon_type:"",
		weapon_damage:0,
      },
	  activeLocation: {
        location_name: "",
        enemy_type: "",
		min_level: 0,
		nr_public_events:0,
		nr_lost_sectors:0,
      },
	  activeLogin:{
		  username: "",
		  password1:"",
	  },
	  
    };
  }
  
   handleChange = (e) => {
    let { name, value } = e.target;
    console.log(name);
	this.setState({filterValue: value});
    //this.state.filterValue = value;
  };
  
  componentDidMount() {
    this.refreshList();
  }

  refreshList = () => {
    axios
      .get("/api/players/")
      .then((res) => this.setState({ players: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, totalItems: res.data.count }))
      .catch((err) => console.log(err));
    axios
      .get("/api/weapons/")
      .then((res) => this.setState({ weapons: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, totalItems: res.data.count }))
      .catch((err) => console.log(err));
    axios
      .get("/api/location/")
      .then((res) => this.setState({ locations: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, totalItems: res.data.count }))
      .catch((err) => console.log(err));

  };
  
  paginate = () => {
	  
	 let newPage = this.state.currentPage;
	 let toDisplay = [];
	 let maxItems = Math.ceil(this.state.totalItems / this.state.perPage);
	 
	toDisplay.push(1);
	toDisplay.push(2);
	
	if(newPage > 3 && newPage < maxItems - 2){
	toDisplay.push(newPage - 1);
	toDisplay.push(newPage);
	toDisplay.push(newPage + 1);
	}
	if(newPage === 3){ 
	toDisplay.push(newPage);
	toDisplay.push(newPage+1);
	}
	if(newPage === 2){ 
	toDisplay.push(newPage+1);
	}
	
	if(newPage === maxItems - 2){ 
	toDisplay.push(newPage-1);
	toDisplay.push(newPage);
	}
	if(newPage === maxItems - 1){ 
	toDisplay.push(newPage-1);
	}
	
	toDisplay.push(maxItems - 1);
	toDisplay.push(maxItems);
	
	return toDisplay.map((number) => (
   <button className="btn btn-primary" onClick={()=>this.paginationHandler(number)}>{number}</button>
    )); 
    	
	  
  };
  
  toggle = () => {
    this.setState({ modal: !this.state.modal });
  };
  toggleWeapon = () => {
    this.setState({ modal_weapon: !this.state.modal_weapon });
  };
    toggleLocation = () => {
    this.setState({ modal_location: !this.state.modal_location });
  };
    toggleLogin = () => {
    this.setState({ modal_login: !this.state.modal_login });
  };

  handleSubmit = (item) => {
    this.toggle();
	let classes1 = ["Warlock", "Hunter", "Titan"];
	if(!classes1.includes(item.class1)){
		document.getElementById("error1").innerHTML = "Class must be Warlock, Hunter or Titan.";
		return;
	}
    
    if (item.id) {
		document.getElementById("error1").innerHTML = "";
      axios
        .put(`/api/players/${item.id}`, item)
        .then((res) => this.refreshList());
      return;
    }
	document.getElementById("error1").innerHTML = "";
    axios
      .post("/api/players/", item)
      .then((res) => this.refreshList());
  };
  handleSubmitWeapon = (item) => {
    this.toggleWeapon();
	
	let slotTypes = ["Kinetic", "Energy", "Heavy"];
	let elements1 = ["Arc", "Solar", "Void", "Stasis", "Strand"];
	let errorMsg = "";
	if(!slotTypes.includes(item.weapon_slot)){
		errorMsg += "Slot must be Kinetic, Energy or Heavy.";
	}
	if(!elements1.includes(item.weapon_element)){
		errorMsg += "Element must be Arc,Solar,Void,Stasis,Strand.";
	}
    
	if(errorMsg !== ""){
		document.getElementById("error1").innerHTML = errorMsg;
		return;
	}
    if (item.id) {
	  document.getElementById("error1").innerHTML = "";
      axios
        .put(`/api/weapons/${item.id}`, item)
        .then((res) => this.refreshList());
      return;
    }
	document.getElementById("error1").innerHTML = "";
    axios
      .post("/api/weapons/", item)
      .then((res) => this.refreshList());
  };
  handleSubmitLocation = (item) => {
    this.toggleLocation();
    let enemies1 = ["Fallen", "Scorn", "Cabal", "Vex", "Taken"];
	let errorMsg = "";
	
	if(!enemies1.includes(item.enemy_type)){
		errorMsg += "Enemy must be Falle, Scorn, Cabal, Vex, Taken.";
	}
	if(item.nr_lost_sectors < 3){
		errorMsg += "Lost sectors must be at least 3.";
	}
	if(item.min_level < 1){
		errorMsg += "Min level must be at least 1.";
	}
	if(errorMsg !== ""){
		document.getElementById("error1").innerHTML = errorMsg;
		return;
	}
    if (item.id) {
	  document.getElementById("error1").innerHTML = "";
      axios
        .put(`/api/location/${item.id}`, item)
        .then((res) => this.refreshList());
      return;
    }
	document.getElementById("error1").innerHTML = "";
    axios
      .post("/api/location/", item)
      .then((res) => this.refreshList());
  };
  handleLogin = (item) => {
    this.toggleLogin();
	let errorMsg = "";
	
	document.getElementById("error1").innerHTML = errorMsg;
    axios
      .post("/api/register", item)
      .then((res) => this.refreshList());
  };
  
   getWeapons = () => {
	   this.setState({currentPage:1});
	this.setState({viewCompleted: 5});
    axios
      .get("/api/weapons/")
      .then((res) => this.setState({ weapons: res.data.results }))
      .catch((err) => console.log(err));
  };
   getLocations = () => {
	   this.setState({currentPage:1});
	this.setState({viewCompleted: 6});
    axios
      .get("/api/location/")
      .then((res) => this.setState({ locations: res.data.results }))
      .catch((err) => console.log(err));
  };
  
  getReport = () => {
	//this.state.viewCompleted = 3;
	this.setState({currentPage:1});
	this.setState({viewCompleted: 3});
    axios
      .get("/api/report/")
      .then((res) => this.setState({ reportPlayers: res.data.results }))
      .catch((err) => console.log(err));
  };
  
  getFilter = (val) => {
	//this.state.viewCompleted = 4;
	this.setState({currentPage:1});
	this.setState({viewCompleted: 4});
    axios
      .get(`/api/location/filter/${val}`)
      .then((res) => this.setState({ filterPlayers: res.data.results }))
      .catch((err) => console.log(err));
  };

  handleDelete = (item) => {
    axios
      .delete(`/api/players/${item.id}`)
      .then((res) => this.refreshList());
  };
    handleDeleteWeapon = (item) => {
    axios
      .delete(`/api/weapons/${item.id}`)
      .then((res) => this.refreshList());
  };
    handleDeleteLocation = (item) => {
    axios
      .delete(`/api/location/${item.id}`)
      .then((res) => this.refreshList());
  };

  createItem = () => {
    const item = { name: "", class1: "", level: 0, glimmer: 0, shards: 0 };

    this.setState({ activeItem: item, modal: !this.state.modal, modal_type: 0 });
  };
  
  createWeapon = () => {
    const item = { weapon_name: "", weapon_slot: "", weapon_element: "", weapon_type: "", weapon_damage: 0 };
    
    this.setState({ activeWeapon: item, modal_weapon: !this.state.modal_weapon, modal_type: 1 });
  };
  
  createLocation = () => {
    const item = { location_name: "", enemy_type: "", min_level: 0, nr_public_events: 0, nr_lost_sectors: 0 };
    
    this.setState({ activeLocation: item, modal_location: !this.state.modal_location, modal_type: 2 });
  };
  createLogin = () => {
    const item = { username: "", password1: ""};
    
    this.setState({ activeLogin: item, modal_login: !this.state.modal_login, modal_type: 3 });
  };

  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal , modal_type: 0});
  };
  
  editWeapon = (item) => {
    this.setState({ activeWeapon: item, modal_weapon: !this.state.modal_weapon, modal_type: 1 });
  };
  
  editLocation = (item) => {
    this.setState({ activeLocation: item, modal_location: !this.state.modal_location, modal_type: 2 });
  };
  

  displayCompleted = (status) => {
	  this.setState({currentPage:1});
	  this.refreshList();
	return this.setState({ viewCompleted: status });
  };
  
  paginationHandler=(pg)=>{ 
  //let str = url;
  //let subStr = str.substring(0, str.indexOf('='));
  //let newStr = str.replace(subStr,"");
  //console.log(newStr);
  	let url1 = "";
	switch(this.state.viewCompleted){
        case 1:
		url1 = `/api/players/?page=`;
		break;
		case 2:
		url1 = `/api/players/?page=`;
		break;
		case 3:
		url1 = "/api/report/?page=";
		break;
		case 4:
		let val = this.state.filterValue;
		url1 = `/api/location/filter/${val}?page=`;
		break;
		case 5:
		url1 = `/api/weapons/?page=`;
		break;
		case 6:
		url1 = `/api/location/?page=`;
		break;
	    default:
		url1 = `/api/players/?page=`;
		break;
		
	}
  try{
	  if(this.state.viewCompleted === 1 || this.state.viewCompleted === 2){
	  axios.get(url1+pg)
	  .then((res)=>{this.setState({ players: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, currentPage: pg})  
	  });
	  }
	  if(this.state.viewCompleted === 3){
	  axios.get(url1+pg)
	  .then((res)=>{this.setState({ reportPlayers: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, currentPage: pg})  
	  });
	  }
	  	  if(this.state.viewCompleted === 4){
	  axios.get(url1+pg)
	  .then((res)=>{this.setState({ filterPlayers: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, currentPage: pg})  
	  });
	  }
	  	  if(this.state.viewCompleted === 5){
	  axios.get(url1+pg)
	  .then((res)=>{this.setState({ weapons: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, currentPage: pg})  
	  });
	  }
	  	  if(this.state.viewCompleted === 6){
	  axios.get(url1+pg)
	  .then((res)=>{this.setState({ locations: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, currentPage: pg})  
	  });
	  }
  }catch(error){
	  console.log(error);
  }
  }

  renderTabList = () => {
    return (
      <div className="nav nav-tabs">
        <span
          className={this.state.viewCompleted === 1 ? "nav-link active" : "nav-link"}
          onClick={() => this.displayCompleted(1)}
        >
          Players
        </span>
		
		<span
          className={this.state.viewCompleted === 5 ? "nav-link active" : "nav-link"}
          onClick={() => this.getWeapons()}
        >
          Weapons
        </span>
		
		<span
          className={this.state.viewCompleted === 6 ? "nav-link active" : "nav-link"}
          onClick={() => this.getLocations()}
        >
          Locations
        </span>
		
        <span
          className={this.state.viewCompleted === 2? "nav-link active" : "nav-link"}
          onClick={() => this.displayCompleted(2)}
        >
          Sorted Players
        </span>
		<span
          className={this.state.viewCompleted === 3? "nav-link active" : "nav-link"}
          onClick={() => this.getReport()}
        >
          Statistical Report
        </span>
		<span
          className={this.state.viewCompleted === 4? "nav-link active" : "nav-link"}
          onClick={() => this.getFilter(this.state.filterValue)}
        >
          Filter
        </span>
      </div>
    );
  };

  renderItems = () => {
    const { viewCompleted } = this.state;
	let newItems = 0;
	if(viewCompleted === 1)
   // newItems = this.state.players.filter(
   //   (item) => item.name != "");
   newItems = this.state.players;
    
	if(viewCompleted === 2)
		newItems = [...this.state.players].sort((a, b) => b.level - a.level);
	
	if(viewCompleted === 3){
		newItems = this.state.reportPlayers;
	}
	if(viewCompleted === 4){
		newItems = this.state.filterPlayers;
	}
	if(viewCompleted === 5){
		newItems = this.state.weapons;
	}
	if(viewCompleted === 6){
		newItems = this.state.locations;
	}
	
	if(viewCompleted !== 3 && viewCompleted !== 4 && viewCompleted !== 5 && viewCompleted !== 6){ 
    return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          title={item.name}
        >
          {item.name + "/" + item.class1 + "/" + item.nr_weapons}
        </span>
        <span>
          <button
            className="btn btn-secondary mr-2"
			onClick={() => this.editItem(item)}
          >
            Edit
          </button>
          <button
            className="btn btn-danger"
			onClick={() => this.handleDelete(item)}
          >
            Delete
          </button>
        </span>
      </li>
    ));
	}
	else{ 
	if(viewCompleted === 3){ 
		 return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          className={`todo-title mr-2 ${
            this.state.viewCompleted ? "completed-todo" : ""
          }`}
          title={item.name}
        >
          {item.name + "/" + item.avg_weapon_dmg}
        </span>
      </li>
    ));
	}
	if(viewCompleted === 4){
				 return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          className={`todo-title mr-2 ${
            this.state.viewCompleted ? "completed-todo" : ""
          }`}
          title={item.name}
        >
          {item.location_name}
        </span>
      </li>
    ));
	}
	
	if(viewCompleted === 5){ //weapons
				 return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          className={`todo-title mr-2 ${
            this.state.viewCompleted ? "completed-todo" : ""
          }`}
          title={item.name}
        >
          {item.weapon_name + "/" + item.weapon_damage}
        </span>
		<span>
          <button
            className="btn btn-secondary mr-2"
			onClick={() => this.editWeapon(item)}
          >
            Edit
          </button>
          <button
            className="btn btn-danger"
			onClick={() => this.handleDeleteWeapon(item)}
          >
            Delete
          </button>
        </span>
		
      </li>
    ));
	}
	if(viewCompleted === 6){ //locations
				 return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          className={`todo-title mr-2 ${
            this.state.viewCompleted ? "completed-todo" : ""
          }`}
          title={item.name}
        >
          {item.location_name + "/" + item.nr_public_events}
        </span>
		
		<span>
          <button
            className="btn btn-secondary mr-2"
			onClick={() => this.editLocation(item)}
          >
            Edit
          </button>
          <button
            className="btn btn-danger"
			onClick={() => this.handleDeleteLocation(item)}
          >
            Delete
          </button>
        </span>
      </li>
    ));
	}

	}
  };
  render() {
    return (
      <main className="container">
        <h1 className="text-black text-uppercase text-center my-4">Destiny Characters</h1>
		<p id="error1" className="text-center"></p>
        <div className="row">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="card p-3">
              <div className="mb-4">
			 <FormGroup>
              <Label for="player-filter">Filter zones by level</Label>
			  <Input
                type="number"
                id="player-level"
                name="level"
                onChange={this.handleChange}
                placeholder="0"
                />
				</FormGroup>
                <button
                  className="btn btn-primary"
				  onClick={this.createItem}
                >
                  Add Player
                </button>
				
				<button
                  className="btn btn-primary"
				  onClick={this.createWeapon}
                >
                  Add Weapon
                </button>
				<button
                  className="btn btn-primary"
				  onClick={this.createLocation}
                >
                  Add Location
                </button>
				<button
                  className="btn btn-primary"
				  onClick={this.createLogin}
                >
                  Login
                </button>
			   
              </div>
              {this.renderTabList()}
			  
              <ul className="list-group list-group-flush border-top-0">
                {this.renderItems()}
				
				<li>
				{this.paginate()}
				</li>
				{/*
				<li><button
                  className="btn btn-primary"
				  onClick={()=>this.paginationHandler(this.state.previousUrl)}
                >
				 Previous
                </button>
				
		        <button
                  className="btn btn-primary"
				  onClick={()=>this.paginationHandler(this.state.nextUrl)}
                >
				 Next
                </button></li>
				*/}

              </ul>
            </div>
          </div>
        </div>
		{this.state.modal ? (
          <Modal
		    modal_type={this.state.modal_type}
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleSubmit}
          />
        ) : null}
		{this.state.modal_weapon ? (
          <Modal
		    modal_type={this.state.modal_type}
            activeItem={this.state.activeWeapon}
            toggle={this.toggleWeapon}
            onSave={this.handleSubmitWeapon}
          />
        ) : null}
		{this.state.modal_location ? (
          <Modal
		    modal_type={this.state.modal_type}
            activeItem={this.state.activeLocation}
            toggle={this.toggleLocation}
            onSave={this.handleSubmitLocation}
          />
        ) : null}
		{this.state.modal_login ? (
          <Modal
		    modal_type={this.state.modal_type}
            activeItem={this.state.activeLogin}
            toggle={this.toggleLogin}
            onSave={this.handleLogin}
          />
        ) : null}
		
      </main>
    );
  }
}

export default App;
