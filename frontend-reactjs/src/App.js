// React Stuff
import React from 'react';
import { useState } from 'react';
// Bootstrap CSS
import "bootstrap/dist/css/bootstrap.min.css";
// Bootstrap Bundle JS
import "bootstrap/dist/js/bootstrap.bundle.min";
// Bootstrap Icons
import "bootstrap-icons/font/bootstrap-icons.css";
// Custom CSS
import './App.css';



// Add Google Fonts
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Raleway:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
</style>

function youtube_parser(url) {
  // get video id from url
  if (url === '') {
    console.log('No url was entered');
    return '';
  }
  // Check if url is valid
  if (!url.includes('youtube.com/watch?v=')) {
    console.log('Invalid youtube url entered');
  }
    
  var video_id = url.split('v=')[1];
  var ampersandPosition = video_id.indexOf('&');
  if(ampersandPosition !== -1) {
    video_id = video_id.substring(0, ampersandPosition);
  }
  return video_id;
}


function App() {
  const [url, setUrl] = useState("https://www.youtube.com/watch?v=2L8RXnEFae8");
  const [stats, setStats] = useState({});
  const [comments, setComments] = useState([]);

  const Stats = ({ stats }) => {
    return (
      stats.length > 0 ? (
        <div>
          <div>
            <div>
            <div>
              Comments 
            </div>
            <div>
              {stats.total_comments}
            </div>
          </div>
            <div>
              Likes 
            </div>
            <div>
              <i className="bi bi-heart"></i>{stats.total_likes}
            </div>
          </div>
          <div>
            <div>
              Replies 
            </div>
            <div>
              <i className="bi bi-arrow-return-right"></i>{stats.total_replies}
            </div>
          </div>

          
          <div className="mt-4">
                  Avr polarity <br></br> {stats.avr_polarity} <br></br>
                  Avr subjectivity <br></br>{stats.avr_subjectivity} <br></br>
                  Avr afinn Score <br></br>{stats.avr_afinn_score} <br></br>
          </div>
          </div>
      ) : <> 
          <br></br>
          <div>
            <div className="row p-0">
              <div className="col-sm-4">
                <div className="mx-2 Comment">Comments</div>
                <div className="mx-2 p-1 Comment">{stats.total_comments}</div>
              </div>
               <div className="col-sm-4">
                <div className="mx-2 Comment">Likes</div>
                <div className="mx-2 p-1 Comment">{stats.total_likes}</div>
              </div>
               <div className="col-sm-4">
                <div className="mx-2 Comment">Replies</div>
                <div className="mx-2 p-1 Comment">{stats.total_replies}</div>
              </div>
              </div>
            <div className="row mt-4 p-0">
              <div className="col-sm-4">
                <div className="mx-2">Polarity</div>
                <hr className="mx-2 my-1"></hr>
                <div className="mx-2 p-1">{stats.avr_polarity}</div>
              </div>
               <div className="col-sm-4">
                <div className="mx-2">Subjectivity</div>
                <hr className="mx-2 my-1"></hr>
                <div className="mx-2 p-1">{stats.avr_subjectivity}</div>
              </div>
              <div className="col-sm-4">
                <div className="mx-2">Afinn</div>
                <hr className="mx-2 my-1"></hr>
                <div className="mx-2">{stats.avr_afinn_score}</div>
              </div>
            </div>
          </div>

        </>
      
      
    );
  };


  // TODO: Try to move this to a separate file (or outside of App function)
  const Comments = ({ comments }) => {
  return (
    <div className='CommentsContainer mt-4'>

      {comments.map((comment, index) => (
        <div className='Comment' key={index}>
          <div className='row'>
              <div className='col-sm-1'>
                <span className='CommentProfilePic'>
                  <img className='CommentProfilePicImg' alt='Profile Pic' src={comment.profile_pic_url}>
                  </img>
                </span>
              </div>
              <div className='col-sm-7 ps-4'>
                <span className='CommentUsername'>{comment.username}</span>
                <br></br>
                <span className='CommentPublishedAt'>{comment.created_at_utc}</span>
              </div>
              <div className='col-sm-4'>
                <span className="CommentLikes"><i className="bi bi-heart"></i> : {comment.reply_count !== null ? comment.reply_count : 0}{comment.like_count}</span>
                <br></br>
                <span className='CommentReplies'><i className="bi bi-arrow-return-right"></i> : {comment.reply_count !== null ? comment.reply_count : 0}</span>
              </div>
          </div>

          {/* Turkish version */}
          
          <div className='row mt-3'>
            <div className="col-sm-1">
              <span className="CommentLanguage ps-4">TR</span>
            </div>
            <div className='col-sm-7'>
              <span className='CommentText'>{comment.text}</span>
            </div>
            <div className="col-sm-4">
              <span className='CommentPolarity'>P : {comment.stats.polarity.toFixed(2)}</span> <br></br>
              <span className='CommentSubjectivity'>S : {comment.stats.subjectivity.toFixed(2)}</span> <br></br>
              <span className='CommentAfinnScore'>A : {comment.stats.afinn.toFixed(2)}</span> <br></br>
            </div>
          </div>
          
          {/* English version */}
          <div className='row mt-3'>
            <div className="col-sm-1">
              <span className="CommentLanguage ps-4">EN</span>
            </div>
            <div className='col-sm-7'>
              <span className='CommentText'>{comment.text_translated}</span>
            </div>
            <div className="col-sm-4">
              <span className='CommentPolarity'>P : {comment.stats.polarity.toFixed(2)}</span> <br></br>
              <span className='CommentSubjectivity'>S : {comment.stats.subjectivity.toFixed(2)}</span> <br></br>
              <span className='CommentAfinnScore'>A : {comment.stats.afinn.toFixed(2)}</span> <br></br>
            </div>
          </div>
        </div>
      ))}

    </div>
  );
};

  const handleChange = (event) => {
    setUrl(event.target.value);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const video_code = youtube_parser(url);
    //const API_ENDPOINT = 'https://youtube-sentiment-analysis.herokuapp.com/api/' + video_code;
    const API_ENDPOINT = 'http://127.0.0.1:5000/api/' + video_code;
    console.log('A video was submitted: ' + video_code);

    const submitButton = document.querySelector('.SubmitButton');
    submitButton.disabled = true;
    submitButton.value = 'Analysing...';


    fetch(API_ENDPOINT, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
      .then(response => response.json())
      .then(data => {
        console.log("data123: ", data);
        const json_data = JSON.parse(data);
        console.log("data123 0 - : ", json_data);
        //setComments(data);
        setStats(json_data.stats);
        setComments(json_data.comments);
        
      })
      .catch(error => {
        console.log("error123: ", error);
      })
  }


  return (
    <div>
      <div className="container p-0">
        <div className="AppTitle">Youtube Sentiment Analysis </div>
        <div className="AppSubtitle">   Get & Analyse video comments easily </div>        
        <div className="row ThreeColumnLayout">
          <div className="col-sm LeftColumn">
            <br></br>
            <iframe width="400" height="300" src="https://www.youtube.com/embed/2L8RXnEFae8" title="iboflows   Tingling Brain" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"></iframe>

            <br>
            </br>
            <form onSubmit={handleSubmit} className="MyForm">
              <label>
                <input type="text" value={url}
                  className="TextInput"
                  placeholder=" Enter Youtube URL of the video "
                  onChange={handleChange} />
              </label>
              <br></br>
              <input className="SubmitButton"
                type="submit" value="Analyse Comments" />
            </form>
          </div>
          <div className="col-sm MiddleColumn">
            <Stats stats={stats} />
          </div>
          <div className="col-sm RightColumn">
            <Comments comments={comments} />
          </div>
        </div>
      </div>
    </div>

    
    

  );
}

export default App;
