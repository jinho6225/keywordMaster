import { useState } from 'react';
import './App.css';
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

function App() {
  const [keyword, setKeyword] = useState('');

  const onChange = (e) => {    
    setKeyword(e.target.value)
  }

  const handleSubmit =(e) => {
    e.preventDefault();
    console.log('You clicked submit.');
    // fetch(`http://127.0.0.1:8000/api/blog-keyword`).then(data => data.json()).then(data => console.log(data))
    axios
    .post("http://127.0.0.1:8000/api/blog-keyword", { keyword })
    .then(res => console.log(res, 'data'));
    // axios
    //   .get("http://127.0.0.1:8000/api")
    //   .then(res => console.log(res.data))
    //   .catch(err => console.log(err));
    setKeyword('')
  }

  return (
    <div className="App">
      <form onSubmit={handleSubmit}>
        <label>
          Keyword:
          <input type="text" name="name" value={keyword} placeholder='enter Keyword' onChange={onChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
}

export default App;
