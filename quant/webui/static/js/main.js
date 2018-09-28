//import axios from 'axios';

class Test extends React.Component{
    render=()=> {
        return (
            <div>

            </div>
            )
    }
}
class Right extends React.Component{
    constructor(props) {
        super(props)
        this.state = {
            message:'ok'
        }
    }
    clicked=()=>{
        alert(this.state.message)
        //that = this;
        const _this = this;    //先存一下this，以防使用箭头函数this会指向我们不希望它所指向的对象
        //this.setState({'message':this.state.message+'1'})
        axios.get('http://127.0.0.1:5000/echo/%E4%BD%A0%E5%A5%BD').then(function (resp) {
            console.log(resp.data.message)
            _this.setState({'message':resp.data.message})
        })
    }

    render=()=>{
        return(

    <div></div>
        )
    }
}

class Left extends React.Component{
        render=()=>{
        return (
            <div>

            </div>
            )
    }
}

class Main extends React.Component{
    onClick = ()=>{
    alert('我被点击了');
}

render = ()=>{
        return (
            <div>
                <h1 onClick={this.onClick}>点击我!</h1>
                <Left/>
                <Right/>
            </div>
        )
    }
}

ReactDOM.render(
<Main/>,
    document.getElementById('app')
);
