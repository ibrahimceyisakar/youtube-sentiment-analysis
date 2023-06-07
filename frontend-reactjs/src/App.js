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
              <i className="bi bi-arrow-return-right"></i>{stats.commentgpt_stats}
            </div>
          </div>

          
          <div className="mt-4  font-small">
                  Avr polarity <br></br> {stats.avr_polarity.toFixed(2)} <br></br>
                  Avr subjectivity <br></br>{stats.avr_subjectivity.toFixed(2)} <br></br>
                  Avr afinn Score <br></br>{stats.avr_afinn_score.toFixed(2)} <br></br>
          </div>
          </div>
      ) : <> 
          <br></br>
          <div>
            <div className="row p-0  font-small">
              <div className="col-sm-4">
                <div className="mx-2">Comments<br></br>{stats.total_comments ? stats.total_comments : "..."}</div>
              </div>
               <div className="col-sm-4">
                <div className="mx-2">Likes<br></br>{stats.total_likes ? stats.total_likes : "..."}</div>
              </div>
               <div className="col-sm-4">
                <div className="mx-2">Replies<br></br>{stats.total_reply_count ? stats.total_reply_count : "..."}                
</div>
              </div>
              </div>
            <div className="row mt-4 p-0 font-small">
              <div className="col-sm-4 ">
                <div className="mx-2">Polarity<br></br> {stats.avr_polarity ? stats.avr_polarity.toFixed(2) : "..."
                }</div>
                <div className="mx-2 p-1"></div>
              </div>
               <div className="col-sm-4">
                <div className="mx-2">Subjectivity<br></br>{stats.avr_subjectivity ? stats.avr_subjectivity.toFixed(2) : "..."
                }</div>
                <div className="mx-2 p-1"></div>
              </div>
              <div className="col-sm-4">
                <div className="mx-2">Afinn
                 
                  <br></br>  {stats.avr_afinn_score  ? stats.avr_afinn_score.toFixed(2) : "..."
                  }
                </div>
                <div className="mx-2"></div>
              </div>
            </div>
            <div className="row mt-4 p-0">
              <div className="col-sm-12">
                <div className="mx-2">CommentGPT Response</div>
                <div className="mx-2 p-1 fs-6">{stats.commentgpt_stats}</div>
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
      <div className='row'>
      </div>
      {comments.map((comment, index) => (
        <div className='Comment' key={index}>
          <div className='row'>
              <div className='col-sm-1'>
               <span className='CommentProfilePic'>
                  <img className='CommentProfilePicImg m-1' alt='Profile Pic' src={comment.author_profile_image_url}>
                  </img>
                </span>
              </div>
              <div className='col-sm-3'>
                <span className='CommentUsername'>{comment.author_name}</span>
                <br></br>
                <span className='CommentPublishedAt'>{comment.published_at}</span>
              <br></br><br></br>
                <span className='CommentText'>{comment.text}</span>

              </div>
            <div className='col-sm-8'>
               <span className="CommentLikes"><i className="bi bi-heart"></i>: {comment.like_count !== null ? comment.like_count: 0}</span>
                <span class="px-2 py-0"> </span>
                <span className='CommentReplies'><i className="bi bi-arrow-return-right"></i>: {comment.total_reply_count !== null ? comment.total_reply_count: 0}</span>
             <span class="px-2 py-0"> </span>

              <span className='CommentPolarity'>Polarity: {comment.stats.polarity.toFixed(2)}</span> <span class="px-2 py-0"> </span>

              <span className='CommentSubjectivity'>Subjectivity: {comment.stats.subjectivity.toFixed(2)}</span> <span class="px-2 py-0"> </span>

              <span className='CommentAfinnScore'>Affin: {comment.stats.afinn.toFixed(2)}</span> <span class="px-2 py-0"> </span>

              <span className='CommentAfinnScore'>Classification: {comment.commentgpt_stats.sentiment}</span> <span class="px-2 py-0"> </span>

              <span className='CommentAfinnScore'>Score: {comment.commentgpt_stats.score}</span> <span class="px-2 py-0"> </span>

               </div>
          </div>
          
          <div className='row mt-3'>
            <div className="col-sm-1">
            </div>
            <div className='col-sm-3'>
            </div>
            <div className="col-sm-8">
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
        <div className="AppTitle">CommentGPT </div>
        <div className="AppSubtitle"> One-click tool for analyzing YouTube comments sentiments </div>          
        <div className="row">
          <div className="col-sm-12">
            <form onSubmit={handleSubmit} className="MyForm">
              <div class="row">
                <div class="col-sm-8">
                  <input type="text" value={url}
                    className="TextInput ps-4"
                    placeholder=" Enter Youtube URL of the video "
                    onChange={handleChange} />
                </div>
                <div class="col-sm-4">
                  <input className="SubmitButton"
                    type="submit" value="Analyse Comments" />
                  </div>
                </div>
            </form>
          </div>
        </div>

        <div className="row ThreeColumnLayout">
          <div className="col-sm-12 RightColumn">
            <Comments comments={comments} />
          </div>
        </div>
      </div>
    </div>

    
    

  );
}

export default App;
