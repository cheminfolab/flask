const FormulaFormatter = ({formula}) => {
    return(
        <span>{
            formula
            .replace(/\s/g, '')
            .split(/(\d+)/)
            .map((s, i) => i % 2 ? <sub key={i}>{s}</sub> : s)
        }</span>
    )
}

export default FormulaFormatter