
import './App.css';
import Modal from "./components/Modal";
import React, { Component } from "react";
import Table from 'react-bootstrap/Table';
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
	  users: [],
	  
	  filterValue: 0,
	  nextUrl:"",
	  previousUrl:"",
	  modal: false,
	  modal_weapon: false,
	  modal_location: false,
	  modal_login: false,
	  modal_register: false,
	  modal_view: false,
	  modal_token: false,
	  modal_type:0,
	  isAuth: false,
	  
	  
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
		  password:"",
	  },
	  activeRegister:{
		  username: "",
		  password:"",
	  },
	  activeToken:{
		  token:"",
	  },
	  msg:"",
	  profile_username:"",
	  profile_location:"",
	  profile_marital:"",
	  profile_bio:"",
	  profile_age:0,
	  profile_gender:"",
	  
	  profile_password:"",
	  profile_active:false,
	  profile_isStaff:false,
	  profile_isSuperuser:false,
	  profile_role:0,
	  authToken:"",
	  
    };
  }
  //0 - anonim, 1- user, 2-moderator, 3-admin
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
    toggleRegister = () => {
    this.setState({ modal_register: !this.state.modal_register });
  };
      toggleToken = () => {
    this.setState({ modal_token: !this.state.modal_token });
  };

  handleSubmit = (item) => {
    this.toggle();
	if(this.authToken !== null){
	let yourConfig = {
    headers: {
       Authorization: "Bearer " + this.state.authToken
    }
	}
	let classes1 = ["Warlock", "Hunter", "Titan"];
	if(!classes1.includes(item.class1)){
		document.getElementById("error1").innerHTML = "Class must be Warlock, Hunter or Titan.";
		return;
	}
    
    if (item.id) {
		document.getElementById("error1").innerHTML = "";
      axios
        .put(`/api/players/${item.id}`, item, yourConfig)
        .then((res) => this.refreshList());
      return;
    }
	document.getElementById("error1").innerHTML = "";
    axios
      .post("/api/players/", item, yourConfig)
      .then((res) => this.refreshList());
	}
  };
  handleSubmitWeapon = (item) => {
    this.toggleWeapon();
	
		if(this.authToken !== null){
	let yourConfig = {
    headers: {
       Authorization: "Bearer " + this.state.authToken
    }
	}
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
        .put(`/api/weapons/${item.id}`, item, yourConfig)
        .then((res) => this.refreshList());
      return;
    }
	document.getElementById("error1").innerHTML = "";
    axios
      .post("/api/weapons/", item, yourConfig)
      .then((res) => this.refreshList());
		}
  };
  handleSubmitLocation = (item) => {
    this.toggleLocation();
			if(this.authToken !== null){
	let yourConfig = {
    headers: {
       Authorization: "Bearer " + this.state.authToken
    }
	}
    let enemies1 = ["Fallen", "Scorn", "Cabal", "Vex", "Taken"];
	let errorMsg = "";
	
	if(!enemies1.includes(item.enemy_type)){
		errorMsg += "Enemy must be Fallen, Scorn, Cabal, Vex, Taken.";
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
        .put(`/api/location/${item.id}`, item, yourConfig)
        .then((res) => this.refreshList());
      return;
    }
	document.getElementById("error1").innerHTML = "";
    axios
      .post("/api/location/", item, yourConfig)
      .post("/api/location/", item, yourConfig)
      .then((res) => this.refreshList());
			}
  };
  
  
  getProfile = async() => {
	
	if(this.state.authToken !== null){ 
	let yourConfig = {
    headers: {
       Authorization: "Bearer " + this.state.authToken
    }
	}
		axios.interceptors.response.use(x => { 
	console.log(x);
	return x;
	});
	
	await axios
      .get("/api/profile/", yourConfig)
      	  .then((res) => this.setState({profile_username: res.data.user.username, profile_password: res.data.user.password , profile_active : res.data.isActive, 
		  profile_bio: res.data.bio, profile_age: res.data.age, profile_gender: res.data.gender, profile_marital: res.data.marital_status}, () => {
		  document.getElementById("username").innerHTML = "Username: " + this.state.profile_username;
		  document.getElementById("bio").innerHTML = "Bio: " + this.state.profile_bio;
		  document.getElementById("age").innerHTML = "Age: " +this.state.profile_age;
		  document.getElementById("location").innerHTML = "Location: " +this.state.profile_location;
		  document.getElementById("gender").innerHTML = "Gender: " +this.state.profile_gender;
		  document.getElementById("marital_status").innerHTML = "Status: " +this.state.profile_marital;
		  if(this.state.profile_isSuperuser === true){
			  document.getElementById("role").innerHTML = "Role: admin";
		  }
		  else{ 
		      document.getElementById("role").innerHTML = "Role: user";
		  }
	  }));
	  
	}
	else{ 
	console.log("You are not logged in");
	}
  };
  
  handleLogin = async(item) => {

    this.toggleLogin();
	//let [user, setUser] = useState(null)
    //let [authTokens, setAuthTokens] = useState(null)

	console.log(item.username + "," + item.password);
    await axios
      .post("/api/login/", item)
      	  .then((res) => this.setState({authToken: res.data.access, profile_isSuperuser: res.data.user.is_superuser}, () => {
		   if(this.state.authToken !== null){
			   this.setState({isAuth: true});
			   this.getProfile();
		   }
	  }))
	  .catch((err) => console.log(err));
	  
	  
	//console.log(this.state.authToken)
	//document.getElementById("error1").innerHTML = this.state.authToken;
  };
  
  handleRegister = async(item) => {

    this.toggleRegister();
	console.log(item.username + "," + item.password);
	axios.interceptors.response.use(x => { 
	console.log(x);
	return x;
	});
	
    await axios
      .post("/api/register/", item)
	  .then((res) => this.setState({authToken: res.data.access}, () => {
		    document.getElementById("error1").innerHTML = this.state.authToken;
		  	const newToken = { token: this.state.authToken };
	        this.setState({activeToken: newToken});
	        this.setState({modal_type : 6});
	        this.toggleToken();
	  }));
	  

  };
  
   handleActivation = async(item) => {

    this.toggleToken();
	//let [user, setUser] = useState(null)
    //let [authTokens, setAuthTokens] = useState(null)
	axios.interceptors.response.use(x => { 
	console.log(x);
	return x;
	});
	
    await axios
      .post("/api/token/activate/", item)
	  .then((res) => this.setState({msg: res.data.message}, () => {
		  console.log("User activated. You can log in now.");
		  //document.getElementById("error1").innerHTML = this.state.authToken;
	  }));
	  
  };
  
  
  
   getWeapons = () => {
	this.setState({currentPage:1});
	this.setState({viewCompleted: 5});
    axios
      .get("/api/weapons/")
      .then((res) => this.setState({ weapons: res.data.results}))
      .catch((err) => console.log(err));
  };
  
  
    getUsers = async() => {
	if(this.state.profile_isSuperuser === true){
	this.setState({currentPage:1});
	await axios
      .get("/api/users/")
      .then((res) => this.setState({ users: res.data.results , totalItems: res.data.count}))
      .catch((err) => console.log(err));
	  
	this.setState({viewCompleted: 7}, () => {

	console.log(this.state.totalItems);
	}
	);

	}
	else{
		console.log("You are not an admin");
	}
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
    const item = { username: "", password: ""};
    
    this.setState({ activeLogin: item, modal_login: !this.state.modal_login, modal_type: 3 });
  };
  createRegister = () => {
    const item = { username: "", password: ""};
    
    this.setState({ activeRegister: item, modal_register: !this.state.modal_register, modal_type: 5 });
  };



  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal , modal_type: 0});
  };
  handleProfile = (item) => {
    this.setState({ activeLogin: item, modal_login: !this.state.modal_login , modal_type: 4});
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
  
    handleProfilePage = (e) => {
    e.preventDefault();
    console.log('The link was clicked.');
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
		case 7:
		url1 = `/api/users/?page=`;
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
	  	  	  if(this.state.viewCompleted === 7){
	  axios.get(url1+pg)
	  .then((res)=>{this.setState({ users: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next, currentPage: pg})  
	  });
	  }
  }catch(error){
	  console.log(error);
  }
  }
  
  renderTables = () => {
	  if(this.state.viewCompleted === 1 || this.state.viewCompleted === 2){ //player
	  return (
	    <thead>
	    <tr>
		<th>Name</th>
        <th>Class</th>
        <th>Level</th>
		<th>Glimmer</th>
		<th>Shards</th>
        <th>Total weapons</th>
        <th>Operations</th>
        </tr>
        </thead>
	  );
	  }
	  if(this.state.viewCompleted === 3){ //report
	  return (
	    <thead>
	    <tr>
		<th>Name</th>
        <th>Average weapon damage</th>
        </tr>
        </thead>
	  );
	  }
	  if(this.state.viewCompleted === 4){ //location filter
	  return (
	    <thead>
	    <tr>
		<th>Location Name</th>
        <th>Enemy type</th>
		<th>Minimum Level</th>
		<th>Total Public Events</th>
		<th>Total Lost Sectors</th>
		<th>Operations</th>
        </tr>
        </thead>
	  );
	  }
	  if(this.state.viewCompleted === 5){ //weapons
	  return (
	    <thead>
	    <tr>
		<th>Weapon Name</th>
        <th>Weapon Slot</th>
		<th>Weapon Element</th>
		<th>Weapon Type</th>
		<th>Weapon Damage</th>
		<th>Operations</th>
        </tr>
        </thead>
	  );
	  }
	  if(this.state.viewCompleted === 6){ //locations
	  return (
	    <thead>
	    <tr>
		<th>Location Name</th>
        <th>Enemy type</th>
		<th>Minimum Level</th>
		<th>Total Public Events</th>
		<th>Total Lost Sectors</th>
        </tr>
        </thead>
	  );
	  }
	  if(this.state.viewCompleted === 7){ //users
	  return (
	    <thead>
	    <tr>
		<th>Username</th>
        <th>Location</th>
		<th>Age</th>
		<th>Gender</th>
		<th>Marital Status</th>
        </tr>
        </thead>
	  );
	  }
	  
  };

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
		<span
          className={this.state.viewCompleted === 7? "nav-link active" : "nav-link"}
          onClick={() => this.getUsers()}
		  disabled={this.state.profile_isSuperuser === false}
        >
          Users
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
	if(viewCompleted === 7){
		newItems = this.state.users;
	}
	//let item_creator = "admin"
	//const item_creator_obj = { username: item_creator, password1: item_creator};
	if(viewCompleted !== 3 && viewCompleted !== 4 && viewCompleted !== 5 && viewCompleted !== 6 && viewCompleted !== 7){ 
    return newItems.map((item) => (
	<tr>
          <td>{item.name}</td>
          <td>{item.class1}</td>
		  <td>{item.level}</td>
          <td>{item.glimmer}</td>
		  <td>{item.shards}</td>
		  <td>{item.nr_weapons}</td>
		  
		  <td>
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
		  </td>
    </tr>
	
    ));
	}
	else{ 
	if(viewCompleted === 3){ 
		 return newItems.map((item) => (
		 
		 <tr>
          <td>{item.name}</td>
          <td>{item.avg_weapon_dmg !== null ? item.avg_weapon_dmg : "No weapons"}</td>
        </tr>
    ));
	}
	if(viewCompleted === 4){ //filter location
	return newItems.map((item) => (
		  <tr>
          <td>{item.location_name}</td>
          <td>{item.enemy_type}</td>
		  <td>{item.min_level}</td>
          <td>{item.nr_public_events}</td>
		  <td>{item.nr_lost_sectors}</td>
		
    </tr>

    ));
	}
	
	if(viewCompleted === 5){ //weapons
				 return newItems.map((item) => (
				 
		  <tr>
          <td>{item.weapon_name}</td>
          <td>{item.weapon_slot}</td>
		  <td>{item.weapon_element}</td>
          <td>{item.weapon_type}</td>
		  <td>{item.weapon_damage}</td>
		  
		  <td>
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
		  </td>
    </tr>
    ));
	}
	if(viewCompleted === 6){ //locations
				 return newItems.map((item) => (
      		  <tr>
          <td>{item.location_name}</td>
          <td>{item.enemy_type}</td>
		  <td>{item.min_level}</td>
          <td>{item.nr_public_events}</td>
		  <td>{item.nr_lost_sectors}</td>
		  
		  <td>
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
		  </td>
    </tr>
    ));
	}
	console.log(viewCompleted);
		if(viewCompleted === 7){ //locations
				 return newItems.map((item) => (
      		  <tr>
          <td>{item.user.username}</td>
          <td>{item.location}</td>
		  <td>{item.age}</td>
          <td>{item.gender}</td>
		  <td>{item.marital_status}</td>
		  <td>
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
		  </td>
    </tr>
    ));
	}

	}
  };
  render() {
    return (
      <main className="container">
        <h1 className="text-black text-uppercase text-center my-4">Destiny Characters</h1>
		<p id="error1" className="text-left"></p>
		<div class="card" style={{ width: '18rem' }}>
		<p id="username" className="text-right">Anonymous user</p>
		<p id="bio" className="text-right"></p>
		<p id="location" className="text-right"></p>
		<p id="marital_status" className="text-right"></p>
		<p id="age" className="text-right"></p>
		<p id="gender" className="text-right"></p>
		<p id="role" className="text-right"></p>
		</div>
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
				<button
                  className="btn btn-primary"
				  onClick={this.createRegister}
                >
                  Register
                </button>

			   
              </div>
              {this.renderTabList()}
			  
              <ul className="list-group list-group-flush border-top-0">
			  <Table striped bordered hover>
			  {this.renderTables()}
               <tbody>
	           {this.renderItems()}
                </tbody>
               </Table>
        

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
		{this.state.modal_register ? (
          <Modal
		    modal_type={this.state.modal_type}
            activeItem={this.state.activeRegister}
            toggle={this.toggleRegister}
            onSave={this.handleRegister}
          />
        ) : null}
		{this.state.modal_token ? (
          <Modal
		    modal_type={this.state.modal_type}
            activeItem={this.state.activeToken}
            toggle={this.toggleToken}
            onSave={this.handleActivation}
          />
        ) : null}
		
      </main>
    );
  }
}

export default App;
