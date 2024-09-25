/* eslint-disable react/prop-types */

import React from "react"

function ModalNewChat({ isOpen, onClose, setActualModel }) {
    
    const [modelName, setModelName] = React.useState('')
    const [modelConfs, setModelConfs] = React.useState('')

    const handleGen = async () => {
        try{
            await fetch('http://192.168.0.14:5000/api/newmodel' , {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                },
                body: JSON.stringify({ 'name': modelName,'act_as': modelConfs})
            })
        } catch (e){
            console.log(e)
        } finally {
            setActualModel(modelName)
        }

    }

    if(isOpen) return (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-gray-400 bg-opacity-50 text-black">
            <div className="bg-white px-20 py-8 rounded-xl border-2 border-black text-center">
                <h2 className="mb-2 font-bold text-3xl">Criar um novo modelo</h2>
                <p>Escreva como o modelo deverá se chamar</p>
                <input value={modelName} onChange={(e) => setModelName(e.target.value)} className="border-black border-2 rounded-md px-1 mb-5"/>
                <p>Escreva como o modelo deverá se comportar</p>
                <input value={modelConfs} onChange={(e) => setModelConfs(e.target.value)} className="border-black border-2 rounded-md px-1"/>
                <div className="flex gap-10 justify-center items-center mt-5">
                    <button className="border-2 border-green-800 px-4 rounded-xl bg-green-300" onClick={handleGen}>Criar</button>
                    <button className="border-2 border-red-800 px-4 rounded-xl bg-red-300" onClick={onClose}>Fechar</button>
                </div>
            </div>
        </div>
    );
}


export default ModalNewChat