'use client'

import React, { useState } from 'react';
import { Box, Container, Heading, Input, Text, InputGroup, InputRightElement, Icon, Flex, ChakraProvider, VStack, HStack } from "@chakra-ui/react";
import { ArrowForwardIcon } from "@chakra-ui/icons";
import { FaFutbol } from "react-icons/fa";

export default function Home() {
  const [responses, setResponses] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulating a response. In a real app, you'd make an API call here.
    setResponses([...responses, "This is a sample response. Replace with actual API call results."]);
  };

  return (
    <ChakraProvider>
      <Box as="main" minHeight="100vh" bg="white">
        <Container maxW="container.xl" py={8}>
          <HStack alignItems="flex-start" spacing={8}>

            {/* Left side */}
            <VStack align="stretch" width="50%" spacing={4}>
              <Flex alignItems="center">
                <Icon as={FaFutbol} boxSize={8} mr={2} color="black" />
                <Heading as="h1" size="2xl" color="black">
                  premstats.xyz
                </Heading>
              </Flex>
              <form onSubmit={handleSubmit}>
                <InputGroup size="lg">
                  <Input
                    pr="4.5rem"
                    placeholder="Ask about Premier League stats..."
                    _placeholder={{ color: 'gray.500' }}
                    borderColor="gray.300"
                    bg="gray.100"
                  />
                  <InputRightElement width="4.5rem">
                    <ArrowForwardIcon color="gray.500" boxSize={6} cursor="pointer" onClick={handleSubmit} />
                  </InputRightElement>
                </InputGroup>
              </form>
              <Text color="gray.500" fontSize="sm">
                You can ask the system about any premier league statistic up to but not including the current season
              </Text>
            </VStack>

            {/* Right side */}
            <VStack align="stretch" width="50%" spacing={4}  p={4} borderRadius="md" minHeight="70vh">
              {responses.map((response, index) => (
                <Text key={index} color="gray.800">{response}</Text>
              ))}
            </VStack>
          </HStack>
        </Container>
      </Box>
    </ChakraProvider>
  );
}