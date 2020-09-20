#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aOffset;

mat4 rot90z = mat4(0,1,0,0, -1,0,0,0, 0,0,1,0, 0,0,0,1);

/*int isPrime(int val){
    int i;
    for(i=2; i<=sqrt(val); i++){
        if (val%i == 0) return 0;
    }
    return 1;
}*/

void main()
{
    /*int par = 0, val = gl_InstanceID;
    while (val != 0){
        par ^= val&1;
        val >>= 1;
    }*/
    
    //int par = isPrime(gl_InstanceID);

    int par = int(aOffset.z);

    vec4 apos = vec4(aPos, 1.0);
    if (par==1) apos = rot90z * apos;
    gl_Position = vec4(apos.xyz + vec3(aOffset.xy, 0.0), 1.0);
}
