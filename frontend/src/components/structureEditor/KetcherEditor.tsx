// import { Ketcher } from "ketcher-core"
// import { Editor } from "ketcher-react"
// import { StandaloneStructServiceProvider } from "ketcher-standalone"
// import { useEffect, useState } from "react"
// import "ketcher-react/dist/index.css"

// declare global {
//     interface Window { ketcher: Ketcher}
// }

// const structServiceProvider = new StandaloneStructServiceProvider()

// const KetcherEditor = () => {

//     const [structure, setStructure] = useState<string|null>()
//     const [reaction, setReaction] = useState<string|null>()

//     useEffect(() => {
//         console.log("structure changed:", structure)
//     }, [structure]);

//     useEffect(() => {
//         console.log("reaction changed:", reaction)
//     }, [reaction]);

//     const handleKetcherChange = () => {
//         if (window.ketcher) {
//             if (window.ketcher.containsReaction() === true) {
//                 window.ketcher
//                     .getRxn()
//                     .then((molfile) => setReaction(molfile))
//                     .catch(error => console.error("Error fetching structure:", error))
//             } else {
//                 window.ketcher
//                     .getMolfile()
//                     .then(molfile => setStructure(molfile))
//                     .catch(error => console.error("Error fetching structure:", error))
//             }
//             // const cdxmlfile = await window.ketcher.getCDXml()
//         } else {
//             console.warn("Ketcher instance is not yet available on window.ketcher.")
//         }
//     }

//     const handleClick = () => {
//         if (window.ketcher) {
//             window.ketcher
//                 .layout()
//                 .then(() => console.log("Set layout"))
//                 .catch(error => console.error("Error setting layout:", error))
//         } else {
//             console.warn("Ketcher instance is not yet available on window.ketcher.")
//         }
//     }

//     return (
//         <>
//             <Editor
//                 staticResourcesUrl="/static/"
//                 structServiceProvider={structServiceProvider}
//                 errorHandler={(message: string) => console.error(message)}
//                 onInit={(ketcher) => {
//                     window.ketcher = ketcher
//                     // window.ketcher
//                     //     .setMolecule('CCCCCCCCCC')
//                     //     .catch(e => console.error(e))
//                     window.ketcher.editor.subscribe('change', () => handleKetcherChange())
//                 }}
//                 customButtons={[{id: "1", title: "test", imageLink: ""}]}
//             />
//             <button onClick={() => handleClick()}>layout</button>
//         </>
//     )
// }

// export default KetcherEditor