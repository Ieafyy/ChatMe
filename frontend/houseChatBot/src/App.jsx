import React from "react"
import ChatBar from "./components/ChatBar"
import NewChat from "./components/NewChat"

function App() {

  const [actualModel, setActualModel] = React.useState('Leafy')
  const [responses, setResponses] = React.useState([])


  return (
    <>
    <div className="flex mt-5 justify-between mx-10">
      <h1 className="text-4xl font-bold text-center">{actualModel}</h1>
      <NewChat setActualModel={setActualModel} setResponses={setResponses} actualModel={actualModel}/>
    </div> 
      <ChatBar actualModel={actualModel} responses={responses} setResponses={setResponses}/>
    </>
  )
}

export default App
