<template>
<!-- eslint-disable max-len -->
    <div id="background">
        <div class="container">
            <h1 id= h1>SONG Question Answering  <img src="../assets/question.png" width="50px" height="50px"></h1>
            <hr><br>
            <div class="container-fluid bg-1 text-center">
                <div id="search-container" style="color: whitesmoke;">
                    <form @submit="onSubmit" @reset="onReset">
                        <input id= "question" type="text" placeholder="Question..." v-model="ask.question">
                        <button id = "ask" type="sunmit">Ask</button>
                        <button id = "reset" type="reset">Reset</button>
                    </form>
                </div>
                <div id="answer" v-for="(answer, index) in ans" :key="index">{{ answer.ans }}</div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      question: String,
    };
  },
  methods: {
    getAnswer() {
      const path = 'http://localhost:5000/qa';
      axios.get(path)
        .then((res) => {
          this.answer = res.data.answer;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    askQuestion(payload) {
      const path = 'http://localhost:5000/qa';
      axios.post(path, payload)
        .then(() => {
          this.getAnswer();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getAnswer();
        });
    },
    initForm() {
      this.question = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        question: this.ask.question, // property shorthand
      };
      this.askQuestion(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
  },
  created() {
    this.getAnswer();
  },
};
</script>

<style>
#background {
    right: 0;
    bottom: 0;
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
    z-index: -100;
    font: monospace;
}
#h1{
    color: rosybrown;
    font-family: "Lucida Console", Courier, monospace;
}
#question {
  color: #ffffff;
  font-size: 20px;
  margin-right: 10px;
  border-radius: 15px;
  border: 0px;
  background-color: #f3dcfb;
  background-image: linear-gradient(to bottom right, #f3dcfb, lightskyblue);
  font-family: "Lucida Console", Courier, monospace;
  padding: 25px;
  color:darkslategray;
  float: center;
  width: 620px;
  height: 10px;
}
#search-container {
  float: center;
}
#ask {
  float: center;
  color: white;
  padding: 10px;
  margin-top: 8px;
  margin-right: 10px;
  background: indianred;
  border-radius: 15px;
  font-size: 18px;
  border: none;
  cursor: pointer;
  padding-top: 12px;
  padding-bottom: 12px;
  font-family: "Lucida Console", Courier, monospace;
  padding-left: 18px;
  padding-right: 18px;
}
#ask:hover {
  background: crimson;
}
#reset {
  float: center;
  color: white;
  padding: 10px;
  margin-top: 8px;
  background: cornflowerblue;
  font-family: "Lucida Console", Courier, monospace;
  border-radius: 15px;
  font-size: 18px;
  border: none;
  cursor: pointer;
  padding-top: 12px;
  padding-bottom: 12px;
  padding-left: 12px;
  padding-right: 12px;
}
#reset:hover {
  background: royalblue;
}
#answer {
  float: center;
  background-color: #f3dcfb;
  font-family: "Lucida Console", Courier, monospace;
  border-radius: 15px;
  font-size: 20px;
  width: 620px;
  height: 420px;
  padding: 30px;
  margin-top: 30px;
  margin-left: 150px;
}
</style>
