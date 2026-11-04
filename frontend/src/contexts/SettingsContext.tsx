import {
    createContext,
    type ReactNode
} from "react"

const SettingsContext = createContext({})
export default SettingsContext

export const SettingsProvider = ({children}: {children: ReactNode}) => {
    return(
        <SettingsContext.Provider value={{}}>
            {children}
        </SettingsContext.Provider>
    )
}