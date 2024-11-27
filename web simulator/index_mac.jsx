import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import 'tailwindcss/tailwind.css';
import 'font-awesome/css/font-awesome.min.css';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-javascript.min.js';

const App = () => {
    const [code, setCode] = useState(`start()\nforward(1)\nback(1)\nlanding()`);

    useEffect(() => {
        Prism.highlightAll();
    }, [code]);

    const downloadCode = () => {
        const element = document.createElement("a");
        const file = new Blob([code], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = "code.txt";
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const uploadCode = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            setCode(e.target.result);
        };
        reader.readAsText(file);
    };

    return (
        <div className="flex w-full h-full">
            <div className="flex flex-col items-center justify-center w-1/12 bg-gray-200 p-4">
                <button className="bg-teal-500 text-white rounded-full p-4 mb-4" onClick={downloadCode}>
                    <i className="fas fa-arrow-down"></i>
                </button>
                <label className="bg-teal-500 text-white rounded-full p-4 cursor-pointer">
                    <i className="fas fa-arrow-up"></i>
                    <input type="file" className="hidden" onChange={uploadCode} />
                </label>
            </div>
            <div className="flex-grow grid grid-cols-5 grid-rows-5 border border-gray-300">
                {Array.from({ length: 25 }).map((_, index) => (
                    <div key={index} className="border border-gray-300"></div>
                ))}
                <div className="relative col-start-1 row-start-5 flex items-center justify-center">
                    <img src="https://placehold.co/50x50" alt="Quadcopter image" className="absolute w-12 h-12" />
                </div>
            </div>
            <div className="w-1/3 bg-gray-900 text-white p-4 flex flex-col justify-between">
                <div className="bg-gray-800 rounded-lg p-4 flex-grow shadow-lg">
                    <div className="flex items-center mb-4">
                        <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                        <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    </div>
                    <div className="bg-gray-700 rounded-lg p-4 shadow-inner h-full">
                        <textarea
                            className="w-full h-full bg-transparent text-sm font-mono leading-relaxed text-gray-300 outline-none resize-none"
                            value={code}
                            onChange={(e) => setCode(e.target.value)}
                        />
                        <pre className="hidden">
                            <code className="language-javascript">
                                {code}
                            </code>
                        </pre>
                    </div>
                </div>
                <button className="bg-teal-500 text-white rounded-full p-4 self-center mt-4 shadow-lg hover:bg-teal-600 transition duration-300">
                    Test
                </button>
            </div>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));