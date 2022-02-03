## getting the pre-determined demand pattern
## into a case statement that nuXmv will recognize



pat_demand = [225.63, 218.22, 213.24, 168.47, 150.12, 141.09, 162.9, 152.33, 137.35, 178.19, 203.41, 
159.33, 154.1, 145.61, 150.81, 147.36, 156.01, 209.27, 231.58, 225.83, 204.02, 189.94, 181.96, 
185.94, 194.24, 189.32, 172.79, 162.61, 190.7, 167.92, 174.87, 148.21, 163.19, 205.84, 223.24, 
214.31, 213.73, 209.69, 206.59, 204.99, 188.15, 165.15, 133.81, 99.41, 109.16, 131.2, 147.63, 142.28, 
145.89, 160.4, 219.03, 194.77, 117.73, 117.06, 155.56, 158.43, 163.77, 166.98, 169.76, 136.42, 140.03, 
140.41, 138.72, 132.2, 175.96, 222.5, 174.03, 195.51, 189.62, 202.98, 217.62, 219.25, 216.18, 192.64, 
178.6, 165.19, 139.36, 138.79, 126.31, 161.89, 178.8, 202.22, 220.64, 211.79, 212.39, 222.93, 213.99, 
209.69, 206.34, 155.0, 152.59, 126.06, 113.79, 140.2, 140.56, 147.45, 131.42, 119.83, 172.86, 174.35, 
123.29, 145.77, 173.07, 181.4, 214.71, 236.04, 227.0, 216.45, 175.62, 161.45, 183.58, 115.56, 104.66, 
98.8, 105.77, 138.79, 162.68, 154.22, 157.98, 206.64, 227.95, 211.81, 191.15, 158.39, 146.7, 136.35, 
124.76, 129.84, 161.91, 190.04, 199.96, 206.99, 212.79, 209.57, 208.24, 194.11, 169.9, 172.51, 169.11, 
177.39, 199.17, 229.39, 229.61, 217.96, 213.37, 185.32, 161.81, 138.95, 134.49, 122.39, 82.22, 56.88, 
80.95, 149.83, 151.24, 137.11, 146.01, 143.1, 232.99, 225.16, 201.02, 178.87, 159.68, 191.6, 220.65, 
234.81, 246.29, 241.44, 149.43]

normalized = pat_demand ./ maximum(pat_demand)

# for real demand
println("next(demand) := case")
for (i,j) in enumerate(normalized)
    println("   next(time) = ",i," : ",round(j,digits=1),";")
end
println("   TRUE:1;")
println("esac;")

# For discretized demand
demandStates = [0,0.25,0.5,0.75,1.0]
println("next(demand) := case")
for (i,j) in enumerate(normalized)
    rounded = demandStates[argmin(abs.(j .- demandStates))]
    println("   next(time) = ",i," : ",Int(rounded*100),";")
end
println("   TRUE:1;")
println("esac;")


