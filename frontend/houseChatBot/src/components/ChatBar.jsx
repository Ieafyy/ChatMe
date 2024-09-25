/* eslint-disable react/prop-types */

import React from "react"

function ChatBar({ actualModel, responses, setResponses }) {

    const [msg, setMsg] = React.useState('')
    const [loading, setLoading] = React.useState(false)

    const handlePost = async () => {
        try{
            console.log(actualModel)
            setLoading(true)
            const res = await fetch('http://192.168.0.14:5000/api/readinput' , {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                },
                body: JSON.stringify({ 'data': msg, 'model': actualModel })
            })
            setMsg('')
            const data = await res.json();
            setResponses(prevResponses => [...prevResponses, { message: msg, response: data }]);

        } catch (e){
            console.log(e)
        } finally {
            setLoading(false)
        }

    }

    return (
        <>
            <div>
                <div className="mx-10 w-screen bg-slate-200 lg:w-11/12 mt-5 max-h-[60vh] overflow-y-auto rounded-lg p-4">
                {responses.map((response, index) => (
                        <div key={index}>
                            <p className="border-b-2 py-2 border-slate-300"><strong style={{color: 'green'}}>Você:</strong> {response.message}</p>
                            <p className="border-b-2 py-2 border-slate-300"><strong style={{color: 'red'}}>{ actualModel }:</strong> {response.response['response']}</p>
                        </div>
                    ) )}
                {loading && <p className="mt-2 font-bold">Carregando...</p>}
                </div>
                <div className="fixed bottom-5 left-1/2 transform -translate-x-1/2 flex items-center w-11/12 gap-10">
                    <input autoComplete='off' disabled={loading} onKeyDown={(e) => {if(e.key == 'Enter') handlePost()}} className="flex-grow border-2 py-1 rounded-lg border-black px-4" type="text" id="msg_enter" name="msg_enter" value={msg} onChange={(e) => setMsg(e.target.value) } />
                    <button disabled={loading} onClick={handlePost} className="rounded-lg border-2 border-black px-5 py-1 hover:bg-slate-200 duration-300">Enviar</button>
                </div>                
            </div>
        </>
    )
}

export default ChatBar