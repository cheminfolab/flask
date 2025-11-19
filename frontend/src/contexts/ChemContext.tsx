import type { ChemContextType, Substance, Unit } from "@/types/chemicals"
import { createContext, useState } from "react"

const ChemContext = createContext<ChemContextType | {}>({})
export default ChemContext

export const ChemProvider = ({children}: any) => {

    let [units, setUnits] = useState<Unit[]>([])
    let [substances, setSubstances] = useState<Substance[]>([])

    let contextData = {
        units,
        setUnits,
        substances,
        setSubstances
    }

    return(
        <ChemContext.Provider value={contextData}>
            {children}
        </ChemContext.Provider>
    )
}