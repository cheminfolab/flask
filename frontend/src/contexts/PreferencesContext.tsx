import { createContext, type ReactNode } from "react"

const PreferencesContext = createContext({})
export default PreferencesContext

const PreferencesProvider = ({children}: {children: ReactNode}) => {
    return(
        <PreferencesContext.Provider value={{}}>
            {children}
        </PreferencesContext.Provider>
    )
}
export {PreferencesProvider}