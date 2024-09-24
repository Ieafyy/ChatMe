import React from "react"
import ModalNewChat from "./ModalNewChat"
import ModalTrade from "./ModalTrade";

function NewChat({ setActualModel, setResponses, actualModel }) {
    
    const [isModalOpen, setIsModalOpen] = React.useState(false);
    const [modalTrade, setModalTrade] = React.useState(false);

    const handleClick = () => {
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setModalTrade(false)
    };


    const handleClickTrade = () => {
        setModalTrade(true)
    }

    const handleClickClear = async () => {
        setResponses([])
        try{
            await fetch('http://192.168.0.14:5000/api/deleteData' , {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                },
                body: JSON.stringify({'apagar': 'memoria'})
            })
        } catch (e){
            console.log(e)
        } finally {
            console.log('memoria apagada!')
        }
    }
    
    return (
        <>
        <div className="flex gap-20">
            <h1 onClick={handleClick} className="text-center text-3xl font-bold hover:text-green-500 hover:scale-105 duration-300">(+) novo Chat</h1>
            <h1 onClick={handleClickTrade} className="text-center text-3xl font-bold hover:text-amber-500 hover:scale-105 duration-300">(/) trocar Chat</h1>
            <h1 onClick={handleClickClear} className="text-center text-3xl font-bold hover:text-red-700 hover:scale-105 duration-300">(-) Limpar memoria</h1>
        </div>
            <ModalNewChat isOpen={isModalOpen} onClose={closeModal} setActualModel={setActualModel} />     
            <ModalTrade isOpen={modalTrade} onClose={closeModal} setActualModel={setActualModel} actualModel={actualModel}/>
        </>

    )
}

export default NewChat