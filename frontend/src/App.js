
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
	  filterValue: 0,
	  nextUrl:"",
	  previousUrl:"",
	  modal: false,
      activeItem: {
        name: "",
        class1: "",
		level: 0,
		glimmer:0,
		shards:0,
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
    console.log(this.previousUrl + " " + this.nextUrl);
  }

  refreshList = () => {
    axios
      .get("/api/players/")
      .then((res) => this.setState({ players: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next }))
      .catch((err) => console.log(err));

  };
  
  toggle = () => {
    this.setState({ modal: !this.state.modal });
  };

  handleSubmit = (item) => {
    this.toggle();

    if (item.id) {
      axios
        .put(`/api/players/${item.id}`, item)
        .then((res) => this.refreshList());
      return;
    }
    axios
      .post("/api/players/", item)
      .then((res) => this.refreshList());
  };
  
  getReport = () => {
	//this.state.viewCompleted = 3;
	this.setState({viewCompleted: 3});
    axios
      .get("/api/report/")
      .then((res) => this.setState({ reportPlayers: res.data }))
      .catch((err) => console.log(err));
  };
  
  getFilter = (val) => {
	//this.state.viewCompleted = 4;
	this.setState({viewCompleted: 4});
    axios
      .get(`/api/location/filter/${val}`)
      .then((res) => this.setState({ filterPlayers: res.data }))
      .catch((err) => console.log(err));
  };

  handleDelete = (item) => {
    axios
      .delete(`/api/players/${item.id}`)
      .then((res) => this.refreshList());
  };

  createItem = () => {
    const item = { name: "", class1: "", level: 0, glimmer: 0, shards: 0 };

    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal });
  };
  

  displayCompleted = (status) => {
	return this.setState({ viewCompleted: status });
  };
  
  paginationHandler=(url)=>{ 
  let str = url;
  let subStr = str.substring(0, str.indexOf('='));
  let newStr = str.replace(subStr,"");
  console.log(newStr);
  try{
	  axios.get(`/api/players/?page`+newStr)
	  .then((res)=>{this.setState({ players: res.data.results, previousUrl: res.data.previous, nextUrl: res.data.next})  
	  });
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
	
	if(viewCompleted !== 3 && viewCompleted !== 4){ 
    return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          title={item.name}
        >
          {item.name + "/" + item.class1}
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
          {item.name}
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

	}
  };
  render() {
    return (
      <main className="container">
        <h1 className="text-white text-uppercase text-center my-4">Destiny Characters</h1>
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
                  Add player
                </button>
			   
              </div>
              {this.renderTabList()}
              <ul className="list-group list-group-flush border-top-0">
                {this.renderItems()}
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
				
              </ul>
            </div>
          </div>
        </div>
		{this.state.modal ? (
          <Modal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleSubmit}
          />
        ) : null}
      </main>
    );
  }
}

export default App;
