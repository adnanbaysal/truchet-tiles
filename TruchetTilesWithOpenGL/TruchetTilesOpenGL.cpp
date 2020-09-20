/*
Works with learnopengl.com code repository: https://github.com/JoeyDeVries/LearnOpenGL
*/

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <learnopengl/filesystem.h>
#include <learnopengl/shader_m.h>
#include <learnopengl/camera.h>
#include <learnopengl/model.h>

#include <iostream>

void framebuffer_size_callback(GLFWwindow* window, int width, int height);

// settings
const unsigned int NUMELM     = 64;
const unsigned int MAXSEQIND  = 2 * NUMELM * (NUMELM-1);
const unsigned int SCR_WIDTH  = NUMELM * (1024/NUMELM - 3);
const unsigned int SCR_HEIGHT = NUMELM * (1024/NUMELM - 3);

unsigned parity(unsigned inp){
    unsigned par = 0;
    while (inp!=0)
    {
        par ^= inp&0x1;
        inp >>= 1;
    }
    return par;
}

unsigned gen_idx4row_col(unsigned row, unsigned col){
    unsigned out = row * (row + 3) / 2;
    out += (col + row) * (col + row +1) / 2;
    out -= row * (row + 1) / 2;
    return out;
}

void fill_index_seq(unsigned *index_seq){
    unsigned row, col;
    for (row=0; row<NUMELM; row++)
        for (col=0; col<NUMELM; col++)
            index_seq[row * NUMELM + col] = gen_idx4row_col(row, col);
}

void fill_integer_seq(unsigned *integer_seq){
    for (unsigned i = 0; i <= MAXSEQIND; i++) integer_seq[i] = i;//sequence of natural numbers 
}

void fill_binary_seq(unsigned *binary_seq, unsigned *integer_seq, unsigned *index_seq){
    for (unsigned i = 0; i < NUMELM * NUMELM; i++) binary_seq[i] = parity(integer_seq[index_seq[i]]);
    //can change parity with another (almost) balanced boolean fnc
}

//fibonacci
//void fill_binary_seq(unsigned *binary_seq){
//    unsigned i, f = 0, g = 1, s = 1;
//    for(i=0; i<MAXSEQIND*MAXSEQIND; i++){
//        binary_seq[i] = parity(s);
//        f = g;
//        g = s;
//        s = f + g;
//    }
//}

//bool isPrime(unsigned inp){
//    unsigned upLim = unsigned(sqrt(inp));
//    for (unsigned i=2; i<=upLim; i++){
//        if (inp%i == 0) return false;
//    }
//    return true;
//}

//primes
//void fill_binary_seq(unsigned *binary_seq){
//    unsigned i = 0, j=2;
//    while(i<MAXSEQIND*MAXSEQIND){
//        while (!isPrime(j)) j++;
//        binary_seq[i] = parity(j);
//        i++;
//        j++;
//    }
//}

//void fill_binary_seq(unsigned *binary_seq){
//    unsigned i = 0, j=2;
//    while(i<MAXSEQIND*MAXSEQIND){
//        while (!isPrime(j)) j++;
//        binary_seq[i] = parity(j);
//        i++;
//        j++;
//    }
//}

int main()
{
    // glfw: initialize and configure
    // ------------------------------
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // uncomment this statement to fix compilation on OS X
#endif

    // glfw window creation
    // --------------------
    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "a", NULL, NULL);
    if (window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    // glad: load all OpenGL function pointers
    // ---------------------------------------
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // build and compile shaders
    // -------------------------
    Shader ourShader("vertex_shader.vs", "fragment_shader.fs");
    
    unsigned index_seq[NUMELM * NUMELM];
    fill_index_seq(index_seq);
    
//    std::cout << "index_seq:\n";
//    for(unsigned i=0;i<NUMELM;i++){
//        for(unsigned j=0;j<NUMELM;j++) std::cout << index_seq[i*NUMELM + j] << " ";
//        std::cout << "\n";
//    }
//    std::cout.flush();
    
    unsigned integer_seq[MAXSEQIND+1];
    fill_integer_seq(integer_seq);
    
//    std::cout << "\ninteger_seq:\n";
//    for(unsigned i=0;i<=MAXSEQIND;i++){
//        std::cout << integer_seq[i] << " ";
//    }
//    std::cout << "\n";
//    std::cout.flush();
    
    unsigned binary_seq[NUMELM * NUMELM];
    fill_binary_seq(binary_seq, integer_seq, index_seq);
    
//    std::cout << "\nbinary_seq:\n";
//    for(unsigned i=0;i<NUMELM;i++){
//        for(unsigned j=0;j<NUMELM;j++) std::cout << binary_seq[i*NUMELM + j] << " ";
//        std::cout << "\n";
//    }
//    std::cout.flush();
    
    float offset = 1.0f / NUMELM;
    glm::vec3 translations[NUMELM*NUMELM];
    int index = 0;
    for (int y = -int(NUMELM); y < int(NUMELM); y += 2)
    {
        for (int x = -int(NUMELM); x < int(NUMELM); x += 2)
        {
            glm::vec3 translation;
            translation.x = float(x) / NUMELM + offset;
            translation.y = float(y) / NUMELM + offset;
            translation.z = float(binary_seq[index]);
            translations[index++] = translation;
        }
    }
    
    unsigned int instanceVBO;
    glGenBuffers(1, &instanceVBO);
    glBindBuffer(GL_ARRAY_BUFFER, instanceVBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(glm::vec3) * NUMELM*NUMELM, &translations[0], GL_STATIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, 0);   
    
    float size = 1.0f / NUMELM;
    float vertices[] = {
        -size,  0.0f, 0.0f,  0.0f, size, 0.0f,   
         0.0f, -size, 0.0f,  size, 0.0f, 0.0f};
    unsigned int VBO, VAO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    // bind the Vertex Array Object first, then bind and set vertex buffer(s), and then configure vertex attributes(s).
    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    
    glEnableVertexAttribArray(1);
    glBindBuffer(GL_ARRAY_BUFFER, instanceVBO); // this attribute comes from a different vertex buffer
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glVertexAttribDivisor(1, 1); // tell OpenGL this is an instanced vertex attribute.

    glBindBuffer(GL_ARRAY_BUFFER, 0); 

    glBindVertexArray(VAO); 
    
    // draw in wireframe
    //glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    float grey = 1.0;
    ourShader.use();
    // render loop
    // -----------
    while (!glfwWindowShouldClose(window))
    {
        glClearColor(grey, grey, grey, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
//        glDrawArrays(GL_LINES, 0, 4);
        glDrawArraysInstanced(GL_LINES, 0, 4, NUMELM*NUMELM); // N*N line tuples of 4 vertices each

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // glfw: terminate, clearing all previously allocated GLFW resources.
    // ------------------------------------------------------------------
    glfwTerminate();
    return 0;
}

// glfw: whenever the window size changed (by OS or user resize) this callback function executes
// ---------------------------------------------------------------------------------------------
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    // make sure the viewport matches the new window dimensions; note that width and 
    // height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height);
}
