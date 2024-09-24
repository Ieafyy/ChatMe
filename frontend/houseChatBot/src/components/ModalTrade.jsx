import React from "react"

function ModalTrade({ isOpen, onClose, setActualModel, actualModel }) {

    const [AllModels, setAllModels] = React.useState([])

    React.useEffect(() => {
        console.log('modal!')
        fetch('http://192.168.0.14:5000/api/getModels').then(response => {
            if (!response.ok) throw new Error('erro!')
            return response.json()  
        }).then(data => {
            console.log(data)
            setAllModels(data['models'])
        })
    }, [])

    const handleChange = (event) => {
        setActualModel(event.target.value);
      };
    

    if (isOpen) return (
        <div className="fixed inset-0 z-10 flex items-center justify-center bg-gray-400 bg-opacity-50">
            <div className="bg-white text-black px-20 py-8 rounded-xl border-2 border-black text-center">
                <h2 className="mb-2 font-bold text-3xl mb-5">Selecione o modelo</h2>
                <select id="dropdown" value={actualModel} onChange={handleChange} className="border-2 border-black text-xl mx-5 rounded-xl py-2 px-2 bg-slate-200">
                    {AllModels.map((option) => (
                    <option key={option} value={option}>
                        {option}
                    </option>
                    ))}
                </select>
                <div className="flex gap-10 justify-center items-center mt-5">
                    <button className="border-2 border-green-800 px-4 rounded-xl bg-green-300 mt-5" onClick={onClose}>Confirmar</button>
                </div>
            </div>
        </div>
    );

    else return null
}


export default ModalTrade